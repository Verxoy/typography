"""Объединённый список заявок для менеджеров."""
from __future__ import annotations

from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CallbackRequest
from .chat_services import staff_inbox_chat_queryset
from .models_quotes import QuoteRequest
from .permissions import IsSiteStaff
from .serializers_callbacks import CallbackRequestListSerializer
from .serializers_chat import ChatSessionListSerializer
from .serializers_quotes import QuoteRequestListSerializer


class StaffInboxListView(APIView):
    permission_classes = [IsSiteStaff]

    def get(self, request):
        type_filter = (request.query_params.get('type') or '').strip().lower()
        status_filter = request.query_params.get('status')
        search = (request.query_params.get('search') or '').strip()

        items: list[dict] = []

        if type_filter in ('', 'all', 'quote'):
            qs = QuoteRequest.objects.prefetch_related('attachments').order_by('-created_at')
            if status_filter:
                qs = qs.filter(site_status=status_filter)
            if search:
                qs = qs.filter(
                    models.Q(public_number__icontains=search)
                    | models.Q(company_name__icontains=search)
                    | models.Q(inn__icontains=search)
                    | models.Q(contact_phone__icontains=search)
                    | models.Q(contact_email__icontains=search)
                    | models.Q(contact_name__icontains=search)
                    | models.Q(service_title__icontains=search)
                )
            for row in QuoteRequestListSerializer(qs[:100], many=True).data:
                q = row
                items.append(
                    {
                        **q,
                        'request_type': 'quote',
                        'type_label': 'Быстрый расчёт',
                        'title': q['service_title'],
                        'contact_name': q.get('company_name') or q.get('contact_name', ''),
                        'phone': q['contact_phone'],
                    }
                )

        if type_filter in ('', 'all', 'callback'):
            qs = CallbackRequest.objects.order_by('-created_at')
            if status_filter:
                qs = qs.filter(site_status=status_filter)
            if search:
                qs = qs.filter(
                    models.Q(public_number__icontains=search)
                    | models.Q(name__icontains=search)
                    | models.Q(phone__icontains=search)
                )
            for row in CallbackRequestListSerializer(qs[:100], many=True).data:
                c = row
                items.append(
                    {
                        **c,
                        'title': c['type_label'],
                        'contact_name': c['name'],
                    }
                )

        if type_filter in ('', 'all', 'chat'):
            qs = staff_inbox_chat_queryset().prefetch_related('messages').order_by('-staff_visible_at')
            if status_filter:
                qs = qs.filter(status=status_filter)
            if search:
                qs = qs.filter(
                    models.Q(public_number__icontains=search)
                    | models.Q(visitor_name__icontains=search)
                    | models.Q(email__icontains=search)
                    | models.Q(phone__icontains=search)
                )
            for row in ChatSessionListSerializer(qs[:100], many=True).data:
                listed_at = row.get('staff_visible_at') or row['created_at']
                items.append({**row, 'created_at': listed_at})

        items.sort(key=lambda x: x['created_at'], reverse=True)
        return Response(items[:100])
