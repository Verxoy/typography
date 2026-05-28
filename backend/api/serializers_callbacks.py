from rest_framework import serializers

from .models import CallbackRequest


class CallbackSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallbackRequest
        fields = ['name', 'phone']


class CallbackRequestListSerializer(serializers.ModelSerializer):
    request_type = serializers.SerializerMethodField()
    type_label = serializers.SerializerMethodField()

    class Meta:
        model = CallbackRequest
        fields = [
            'id',
            'public_number',
            'request_type',
            'type_label',
            'name',
            'phone',
            'site_status',
            'bitrix_synced_at',
            'created_at',
        ]

    def get_request_type(self, obj: CallbackRequest) -> str:
        return 'callback'

    def get_type_label(self, obj: CallbackRequest) -> str:
        return obj.request_type_label


class CallbackRequestDetailSerializer(serializers.ModelSerializer):
    site_status_display = serializers.CharField(source='get_site_status_display', read_only=True)
    request_type = serializers.SerializerMethodField()
    type_label = serializers.SerializerMethodField()

    class Meta:
        model = CallbackRequest
        fields = [
            'id',
            'public_number',
            'request_type',
            'type_label',
            'name',
            'phone',
            'site_status',
            'site_status_display',
            'manager_note',
            'bitrix_lead_id',
            'bitrix_synced_at',
            'bitrix_sync_error',
            'bitrix_stub_path',
            'created_at',
        ]

    def get_request_type(self, obj: CallbackRequest) -> str:
        return 'callback'

    def get_type_label(self, obj: CallbackRequest) -> str:
        return obj.request_type_label


class CallbackStaffUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallbackRequest
        fields = ['site_status', 'manager_note']
