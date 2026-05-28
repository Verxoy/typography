from django.db import models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CallbackRequest
from .permissions import IsSiteAdministrator, IsSiteStaff
from .quote_resolve import get_callback_by_ref
from .serializers_callbacks import (
    CallbackRequestDetailSerializer,
    CallbackRequestListSerializer,
    CallbackStaffUpdateSerializer,
)


class StaffCallbackListView(APIView):
    permission_classes = [IsSiteStaff]

    def get(self, request):
        qs = CallbackRequest.objects.order_by('-created_at')
        status_filter = request.query_params.get('status')
        if status_filter:
            qs = qs.filter(site_status=status_filter)
        search = (request.query_params.get('search') or '').strip()
        if search:
            qs = qs.filter(
                models.Q(public_number__icontains=search)
                | models.Q(name__icontains=search)
                | models.Q(phone__icontains=search)
            )
        return Response(CallbackRequestListSerializer(qs[:100], many=True).data)


class StaffCallbackDetailView(APIView):
    permission_classes = [IsSiteStaff]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsSiteAdministrator()]
        return [IsSiteStaff()]

    def get(self, request, ref):
        try:
            callback = get_callback_by_ref(ref)
        except CallbackRequest.DoesNotExist:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CallbackRequestDetailSerializer(callback).data)

    def patch(self, request, ref):
        try:
            callback = get_callback_by_ref(ref)
        except CallbackRequest.DoesNotExist:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        ser = CallbackStaffUpdateSerializer(callback, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        if callback.site_status == CallbackRequest.SiteStatus.CLOSED:
            callback.is_called = True
            callback.save(update_fields=['is_called'])
        return Response(CallbackRequestDetailSerializer(callback).data)

    def delete(self, request, ref):
        try:
            callback = get_callback_by_ref(ref)
        except CallbackRequest.DoesNotExist:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        callback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
