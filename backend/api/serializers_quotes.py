from rest_framework import serializers

from .models_quotes import QuoteAttachment, QuoteRequest
from .quote_attachments import is_image_attachment
from .quote_catalog import get_parameter_rows, get_service


class QuoteSubmitSerializer(serializers.Serializer):
    service_slug = serializers.CharField(max_length=64)
    parameters = serializers.JSONField()
    company_type = serializers.ChoiceField(
        choices=[('ip', 'ИП'), ('ooo', 'ООО'), ('private', 'Частный заказ')]
    )
    company_name = serializers.CharField(max_length=300, required=False, allow_blank=True, default='')
    inn = serializers.CharField(max_length=12, required=False, allow_blank=True, default='')
    contact_name = serializers.CharField(max_length=200)
    contact_phone = serializers.CharField(max_length=32)
    contact_email = serializers.EmailField()
    client_comment = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_inn(self, value):
        digits = ''.join(c for c in (value or '') if c.isdigit())
        if not digits:
            return ''
        if len(digits) not in (10, 12):
            raise serializers.ValidationError('ИНН должен содержать 10 цифр (ООО) или 12 (ИП).')
        return digits

    def validate_service_slug(self, value):
        if not get_service(value):
            raise serializers.ValidationError('Неизвестная услуга.')
        return value

    def validate(self, data):
        company_type = data.get('company_type')
        if company_type == QuoteRequest.CompanyType.PRIVATE:
            data['company_name'] = (data.get('company_name') or '').strip()
            data['inn'] = ''
            return data

        company_name = (data.get('company_name') or '').strip()
        inn = (data.get('inn') or '').strip()
        if not company_name:
            raise serializers.ValidationError({'company_name': 'Укажите название организации.'})
        if not inn:
            raise serializers.ValidationError({'inn': 'Укажите ИНН организации.'})
        data['company_name'] = company_name
        return data


class QuoteAttachmentSerializer(serializers.ModelSerializer):
    is_image = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = QuoteAttachment
        fields = [
            'id',
            'original_name',
            'file_size',
            'content_type',
            'uploaded_at',
            'is_image',
            'download_url',
        ]

    def get_is_image(self, obj: QuoteAttachment) -> bool:
        return is_image_attachment(obj)

    def get_download_url(self, obj: QuoteAttachment) -> str:
        number = obj.quote.public_number if obj.quote_id else str(obj.quote_id)
        return f'/api/staff/quotes/{number}/attachments/{obj.pk}/'


class QuoteRequestListSerializer(serializers.ModelSerializer):
    has_attachments = serializers.SerializerMethodField()

    class Meta:
        model = QuoteRequest
        fields = [
            'id',
            'public_number',
            'service_title',
            'company_name',
            'inn',
            'contact_name',
            'contact_phone',
            'site_status',
            'has_attachments',
            'bitrix_synced_at',
            'created_at',
        ]

    def get_has_attachments(self, obj: QuoteRequest) -> bool:
        if hasattr(obj, '_prefetched_objects_cache') and 'attachments' in obj._prefetched_objects_cache:
            return bool(obj.attachments.all())
        return obj.attachments.exists()


class QuoteRequestDetailSerializer(serializers.ModelSerializer):
    company_type_display = serializers.CharField(source='get_company_type_display', read_only=True)
    site_status_display = serializers.CharField(source='get_site_status_display', read_only=True)
    attachments = QuoteAttachmentSerializer(many=True, read_only=True)
    parameters_labeled = serializers.SerializerMethodField()

    def get_parameters_labeled(self, obj: QuoteRequest) -> list[dict]:
        return get_parameter_rows(obj)

    class Meta:
        model = QuoteRequest
        fields = [
            'id',
            'public_number',
            'service_slug',
            'service_title',
            'parameters',
            'parameters_labeled',
            'company_type',
            'company_type_display',
            'company_name',
            'inn',
            'contact_name',
            'contact_phone',
            'contact_email',
            'client_comment',
            'attachments',
            'site_status',
            'site_status_display',
            'manager_note',
            'bitrix_lead_id',
            'bitrix_synced_at',
            'bitrix_sync_error',
            'bitrix_stub_path',
            'created_at',
        ]


class QuoteStaffUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteRequest
        fields = ['site_status', 'manager_note']
