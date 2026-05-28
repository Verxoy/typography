from django.db import models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .chat_services import assign_manager, manager_reply, staff_inbox_chat_queryset
from .models_chat import ChatSession
from .permissions import IsSiteAdministrator, IsSiteStaff
from .quote_resolve import get_chat_by_ref
from .serializers_chat import (
    ChatManagerMessageSerializer,
    ChatSessionDetailSerializer,
    ChatSessionListSerializer,
    ChatStaffUpdateSerializer,
)


class StaffChatListView(APIView):
    permission_classes = [IsSiteStaff]

    def get(self, request):
        qs = staff_inbox_chat_queryset().prefetch_related('messages').order_by('-staff_visible_at')
        status_filter = request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        search = (request.query_params.get('search') or '').strip()
        if search:
            qs = qs.filter(
                models.Q(public_number__icontains=search)
                | models.Q(visitor_name__icontains=search)
                | models.Q(email__icontains=search)
                | models.Q(phone__icontains=search)
                | models.Q(session_key__icontains=search)
            )
        return Response(ChatSessionListSerializer(qs[:100], many=True).data)


class StaffChatDetailView(APIView):
    permission_classes = [IsSiteStaff]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsSiteAdministrator()]
        return [IsSiteStaff()]

    def get(self, request, ref):
        try:
            session = get_chat_by_ref(ref)
        except ChatSession.DoesNotExist:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        session = ChatSession.objects.prefetch_related('messages').get(pk=session.pk)
        return Response(ChatSessionDetailSerializer(session).data)

    def patch(self, request, ref):
        try:
            session = get_chat_by_ref(ref)
        except ChatSession.DoesNotExist:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)

        ser = ChatStaffUpdateSerializer(session, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        session.refresh_from_db()
        if session.status == ChatSession.Status.IN_PROGRESS and not session.assigned_to_id:
            assign_manager(session, request.user)

        session = ChatSession.objects.prefetch_related('messages').get(pk=session.pk)
        return Response(ChatSessionDetailSerializer(session).data)

    def delete(self, request, ref):
        try:
            session = get_chat_by_ref(ref)
        except ChatSession.DoesNotExist:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffChatReplyView(APIView):
    permission_classes = [IsSiteStaff]

    def post(self, request, ref):
        try:
            session = get_chat_by_ref(ref)
        except ChatSession.DoesNotExist:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)

        if session.status == ChatSession.Status.CLOSED:
            return Response({'detail': 'Чат закрыт.'}, status=status.HTTP_400_BAD_REQUEST)

        ser = ChatManagerMessageSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        manager_reply(session, request.user, ser.validated_data['text'])
        session = ChatSession.objects.prefetch_related('messages').get(pk=session.pk)
        return Response(ChatSessionDetailSerializer(session).data)
