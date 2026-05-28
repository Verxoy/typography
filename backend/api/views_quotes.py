import json

from django.core.exceptions import ValidationError as DjangoValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view, authentication_classes, parser_classes, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models_cms import QuoteServiceConfig
from .quote_catalog import QUOTE_SERVICES, get_service
from .quote_services import create_quote_request
from .serializers_quotes import QuoteSubmitSerializer


class QuoteCatalogView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        cfg = QuoteServiceConfig.get_solo()
        services = cfg.data if cfg.data else QUOTE_SERVICES
        return Response({'services': services})


def _scalar_form_value(value) -> str:
    """MultiPart/QueryDict иногда отдаёт список — DRF ждёт строку."""
    if value is None:
        return ''
    if isinstance(value, list):
        return str(value[0]).strip() if value else ''
    return str(value).strip()


def _parse_submit_payload(raw) -> dict:
    keys = raw.keys() if hasattr(raw, 'keys') else raw
    data = {}
    for key in keys:
        if key in ('layout_files', 'layout_files[]'):
            continue
        raw_val = raw.get(key) if hasattr(raw, 'get') else raw[key]
        data[key] = _scalar_form_value(raw_val)

    params = data.get('parameters', '')
    if isinstance(params, str):
        try:
            data['parameters'] = json.loads(params) if params.strip() else {}
        except json.JSONDecodeError as exc:
            raise ValueError('Некорректный JSON в поле parameters.') from exc
    elif not isinstance(data.get('parameters'), dict):
        data['parameters'] = {}

    return data


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
@parser_classes([MultiPartParser, FormParser])
def quote_submit(request):
    try:
        data = _parse_submit_payload(request.data)
    except ValueError as exc:
        return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    ser = QuoteSubmitSerializer(data=data)
    if not ser.is_valid():
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    validated = ser.validated_data
    service = get_service(validated['service_slug'])

    layout_files = request.FILES.getlist('layout_files')
    if not layout_files:
        layout_files = request.FILES.getlist('layout_files[]')

    try:
        quote = create_quote_request(
            service_slug=validated['service_slug'],
            service_title=service['title'],
            parameters=validated['parameters'],
            company_type=validated['company_type'],
            company_name=validated['company_name'].strip(),
            inn=validated['inn'],
            contact_name=validated['contact_name'].strip(),
            contact_phone=validated['contact_phone'].strip(),
            contact_email=validated['contact_email'].strip().lower(),
            client_comment=(validated.get('client_comment') or '').strip(),
            layout_files=layout_files,
        )
    except DjangoValidationError as exc:
        messages = getattr(exc, 'messages', None)
        detail = messages[0] if messages else str(exc)
        return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {
            'message': (
                'Заявка принята. Точную стоимость рассчитаем и пришлём в коммерческом предложении. '
                'Менеджер свяжется с вами.'
            ),
            'public_number': quote.public_number,
            'created_at': quote.created_at.isoformat(),
            'attachments_count': quote.attachments.count(),
        },
        status=status.HTTP_201_CREATED,
    )
