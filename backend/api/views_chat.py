"""Публичный API чата для виджета на сайте."""
from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.exceptions import ValidationError as DjangoValidationError

from .chat_services import (
    escalate_session,
    get_or_create_session,
    handle_visitor_message,
    session_needs_contact_form,
    submit_contact,
)
from .models_chat import ChatMessage, ChatSession
from .serializers_chat import (
    ChatContactSubmitSerializer,
    ChatEscalateSerializer,
    ChatSessionCreateSerializer,
    ChatSessionPublicSerializer,
    ChatMessageSerializer,
    ChatVisitorMessageSerializer,
)


def _get_session_by_key(key: str) -> ChatSession:
    key = (key or '').strip()
    if not key:
        raise ChatSession.DoesNotExist
    return ChatSession.objects.prefetch_related('messages').get(session_key=key)


class ChatSessionCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = ChatSessionCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        session = get_or_create_session(
            session_key=ser.validated_data.get('session_key') or None,
            page_url=ser.validated_data.get('page_url') or '',
        )
        session = ChatSession.objects.prefetch_related('messages').get(pk=session.pk)
        return Response(ChatSessionPublicSerializer(session).data, status=status.HTTP_200_OK)


class ChatMessageListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, session_key: str):
        try:
            session = _get_session_by_key(session_key)
        except ChatSession.DoesNotExist:
            return Response({'detail': 'Сессия не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        after_id = request.query_params.get('after_id')
        qs = session.messages.order_by('created_at')
        if after_id and str(after_id).isdigit():
            qs = qs.filter(id__gt=int(after_id))

        return Response(
            {
                'session_key': session.session_key,
                'public_number': session.public_number,
                'status': session.status,
                'status_display': session.get_status_display(),
                'visitor_name': session.visitor_name,
                'email': session.email,
                'phone': session.phone,
                'contact_submitted': session.contact_submitted,
                'needs_contact_form': session_needs_contact_form(session),
                'messages': ChatMessageSerializer(qs, many=True).data,
            }
        )


class ChatSendMessageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, session_key: str):
        try:
            session = ChatSession.objects.get(session_key=session_key.strip())
        except ChatSession.DoesNotExist:
            return Response({'detail': 'Сессия не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        ser = ChatVisitorMessageSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        handle_visitor_message(session, ser.validated_data['text'])
        session = ChatSession.objects.prefetch_related('messages').get(pk=session.pk)
        return Response(ChatSessionPublicSerializer(session).data)


class ChatEscalateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, session_key: str):
        try:
            session = ChatSession.objects.get(session_key=session_key.strip())
        except ChatSession.DoesNotExist:
            return Response({'detail': 'Сессия не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        ser = ChatEscalateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        escalate_session(
            session,
            name=ser.validated_data.get('name') or '',
            phone=ser.validated_data.get('phone') or '',
        )
        session = ChatSession.objects.prefetch_related('messages').get(pk=session.pk)
        return Response(ChatSessionPublicSerializer(session).data)


class ChatContactSubmitView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, session_key: str):
        try:
            session = ChatSession.objects.get(session_key=session_key.strip())
        except ChatSession.DoesNotExist:
            return Response({'detail': 'Сессия не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        if session.contact_submitted:
            return Response({'detail': 'Контакты уже отправлены.'}, status=status.HTTP_400_BAD_REQUEST)

        ser = ChatContactSubmitSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            submit_contact(session, **ser.validated_data)
        except DjangoValidationError as exc:
            detail = exc.messages[0] if getattr(exc, 'messages', None) else str(exc)
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)

        session = ChatSession.objects.prefetch_related('messages').get(pk=session.pk)
        return Response(ChatSessionPublicSerializer(session).data)
