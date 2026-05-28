from rest_framework import serializers
from .models import ContactMessage, Resume, CallbackRequest


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'message', 'created_at', 'is_processed']
        read_only_fields = ['id', 'created_at', 'is_processed']


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            'id', 'full_name', 'age', 'education', 'position', 'salary',
            'experience', 'phone', 'created_at', 'is_reviewed',
        ]
        read_only_fields = ['id', 'created_at', 'is_reviewed']


class CallbackRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallbackRequest
        fields = ['id', 'name', 'phone', 'created_at', 'is_called']
        read_only_fields = ['id', 'created_at', 'is_called']
