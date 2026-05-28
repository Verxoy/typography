import logging

from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import ContactMessage, Resume, CallbackRequest
from .callback_services import create_callback_request
from .resume_email import send_resume_notification
from .serializers import ContactMessageSerializer, ResumeSerializer, CallbackRequestSerializer
from .serializers_callbacks import CallbackSubmitSerializer

logger = logging.getLogger(__name__)


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user and request.user.is_staff


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsStaffOrReadOnly]


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsStaffOrReadOnly]


class CallbackRequestViewSet(viewsets.ModelViewSet):
    queryset = CallbackRequest.objects.all()
    serializer_class = CallbackRequestSerializer
    permission_classes = [IsStaffOrReadOnly]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_contact_message(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Сообщение отправлено!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_resume(request):
    serializer = ResumeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    resume = serializer.save()
    try:
        send_resume_notification(resume)
    except Exception as exc:
        logger.exception('Не удалось отправить резюме на почту')
        resume.delete()
        detail = (
            'Не удалось отправить резюме на почту. '
            'Попробуйте позже или свяжитесь с нами по телефону.'
        )
        if settings.DEBUG:
            detail = f'{detail} ({exc})'
        return Response({'detail': detail}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(
        {'message': 'Резюме отправлено! Мы свяжемся с вами в ближайшее время.'},
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def request_callback(request):
    serializer = CallbackSubmitSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    callback = create_callback_request(**serializer.validated_data)
    return Response(
        {
            'message': 'Заявка принята! Мы перезвоним вам в ближайшее время.',
            'public_number': callback.public_number,
        },
        status=status.HTTP_201_CREATED,
    )
