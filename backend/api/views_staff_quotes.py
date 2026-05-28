from django.db import models
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models_quotes import QuoteAttachment, QuoteRequest
from .permissions import IsSiteAdministrator, IsSiteStaff
from .quote_attachments import is_image_attachment
from .quote_resolve import get_quote_by_ref
from .serializers_quotes import (
    QuoteRequestDetailSerializer,
    QuoteRequestListSerializer,
    QuoteStaffUpdateSerializer,
)


def _load_quote(ref: str) -> QuoteRequest:
    return QuoteRequest.objects.prefetch_related('attachments').get(pk=get_quote_by_ref(ref).pk)


class StaffQuoteListView(APIView):
    permission_classes = [IsSiteStaff]

    def get(self, request):
        qs = QuoteRequest.objects.prefetch_related('attachments').order_by('-created_at')
        status_filter = request.query_params.get('status')
        if status_filter:
            qs = qs.filter(site_status=status_filter)
        search = (request.query_params.get('search') or '').strip()
        if search:
            qs = qs.filter(
                models.Q(public_number__icontains=search)
                | models.Q(company_name__icontains=search)
                | models.Q(inn__icontains=search)
                | models.Q(contact_phone__icontains=search)
                | models.Q(contact_email__icontains=search)
            )
        return Response(QuoteRequestListSerializer(qs[:100], many=True).data)


class StaffQuoteDetailView(APIView):
    permission_classes = [IsSiteStaff]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsSiteAdministrator()]
        return [IsSiteStaff()]

    def get(self, request, ref):
        try:
            quote = _load_quote(ref)
        except QuoteRequest.DoesNotExist:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(QuoteRequestDetailSerializer(quote, context={'request': request}).data)

    def patch(self, request, ref):
        try:
            quote = _load_quote(ref)
        except QuoteRequest.DoesNotExist:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        ser = QuoteStaffUpdateSerializer(quote, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(QuoteRequestDetailSerializer(quote, context={'request': request}).data)

    def delete(self, request, ref):
        try:
            quote = get_quote_by_ref(ref)
        except QuoteRequest.DoesNotExist:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        quote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffQuoteAttachmentView(APIView):
    permission_classes = [IsSiteStaff]

    def get(self, request, ref, attachment_id):
        try:
            quote = get_quote_by_ref(ref)
            att = QuoteAttachment.objects.select_related('quote').get(
                pk=attachment_id, quote_id=quote.pk
            )
        except (QuoteRequest.DoesNotExist, QuoteAttachment.DoesNotExist):
            return Response({'detail': 'Файл не найден.'}, status=status.HTTP_404_NOT_FOUND)

        inline = request.query_params.get('inline') == '1' and is_image_attachment(att)
        disposition_type = 'inline' if inline else 'attachment'
        filename = att.original_name.replace('"', "'")

        response = FileResponse(
            att.file.open('rb'),
            as_attachment=not inline,
            filename=att.original_name,
        )
        if att.content_type:
            response['Content-Type'] = att.content_type
        response['Content-Disposition'] = f'{disposition_type}; filename="{filename}"'
        return response
