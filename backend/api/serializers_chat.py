from rest_framework import serializers

from .chat_services import session_needs_contact_form
from .models_chat import ChatMessage, ChatSession


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender_type', 'text', 'created_at']


class ChatSessionPublicSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    messages = ChatMessageSerializer(many=True, read_only=True)
    needs_contact_form = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = [
            'session_key',
            'public_number',
            'visitor_name',
            'email',
            'phone',
            'contact_submitted',
            'needs_contact_form',
            'status',
            'status_display',
            'messages',
            'created_at',
            'updated_at',
        ]

    def get_needs_contact_form(self, obj: ChatSession) -> bool:
        return session_needs_contact_form(obj)


class ChatSessionListSerializer(serializers.ModelSerializer):
    request_type = serializers.SerializerMethodField()
    type_label = serializers.SerializerMethodField()
    site_status = serializers.CharField(source='status')
    site_status_display = serializers.CharField(source='get_status_display', read_only=True)
    contact_name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = [
            'id',
            'public_number',
            'request_type',
            'type_label',
            'title',
            'contact_name',
            'phone',
            'site_status',
            'site_status_display',
            'bitrix_synced_at',
            'contact_submitted',
            'staff_visible_at',
            'created_at',
        ]

    def get_request_type(self, obj: ChatSession) -> str:
        return 'chat'

    def get_type_label(self, obj: ChatSession) -> str:
        return obj.request_type_label

    def get_contact_name(self, obj: ChatSession) -> str:
        return obj.visitor_name or '—'

    def get_title(self, obj: ChatSession) -> str:
        preview = (
            obj.messages.filter(sender_type=ChatMessage.SenderType.VISITOR)
            .order_by('-created_at')
            .values_list('text', flat=True)
            .first()
        )
        if not preview:
            preview = obj.messages.order_by('-created_at').values_list('text', flat=True).first()
        if preview:
            text = preview.replace('\n', ' ')
            return text[:80] + ('…' if len(text) > 80 else '')
        return 'Новый чат'


class ChatSessionDetailSerializer(serializers.ModelSerializer):
    site_status = serializers.CharField(source='status')
    site_status_display = serializers.CharField(source='get_status_display', read_only=True)
    request_type = serializers.SerializerMethodField()
    type_label = serializers.SerializerMethodField()
    assigned_to_username = serializers.CharField(
        source='assigned_to.username',
        read_only=True,
        default='',
    )
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = [
            'id',
            'public_number',
            'session_key',
            'request_type',
            'type_label',
            'visitor_name',
            'email',
            'phone',
            'contact_submitted',
            'page_url',
            'site_status',
            'site_status_display',
            'assigned_to',
            'assigned_to_username',
            'manager_note',
            'escalated_at',
            'bitrix_lead_id',
            'bitrix_synced_at',
            'bitrix_sync_error',
            'bitrix_stub_path',
            'created_at',
            'updated_at',
            'messages',
        ]

    def get_request_type(self, obj: ChatSession) -> str:
        return 'chat'

    def get_type_label(self, obj: ChatSession) -> str:
        return obj.request_type_label


class ChatStaffUpdateSerializer(serializers.ModelSerializer):
    site_status = serializers.CharField(source='status', required=False)

    class Meta:
        model = ChatSession
        fields = ['site_status', 'manager_note']

    def validate_site_status(self, value: str) -> str:
        valid = {c.value for c in ChatSession.Status}
        if value not in valid:
            raise serializers.ValidationError('Недопустимый статус.')
        return value


class ChatVisitorMessageSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=4000)


class ChatEscalateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=32, required=False, allow_blank=True)


class ChatContactSubmitSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=32)


class ChatManagerMessageSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=4000)


class ChatSessionCreateSerializer(serializers.Serializer):
    session_key = serializers.CharField(max_length=64, required=False, allow_blank=True)
    page_url = serializers.CharField(max_length=500, required=False, allow_blank=True)
