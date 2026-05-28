from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from .models_cms import (
    CatalogProduct,
    CatalogProductDetail,
    CatalogSection,
    ChatBotTemplate,
    ChatEscalateKeyword,
    ChatFaqRule,
    GraphicModuleSettings,
    PortfolioWork,
    QuoteServiceConfig,
)
from .roles import GROUP_ADMINISTRATOR, GROUP_MANAGER

User = get_user_model()


class CatalogSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogSection
        fields = (
            'id',
            'section_id',
            'title',
            'home_image_url',
            'sort_order',
            'is_published',
        )


class CatalogProductSerializer(serializers.ModelSerializer):
    section_id = serializers.CharField(source='section.section_id', read_only=True)
    section_title = serializers.CharField(source='section.title', read_only=True)

    class Meta:
        model = CatalogProduct
        fields = (
            'id',
            'section',
            'section_id',
            'section_title',
            'title',
            'slug',
            'image_url',
            'sort_order',
            'is_published',
        )


class CatalogProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogProduct
        fields = (
            'section',
            'title',
            'slug',
            'image_url',
            'sort_order',
            'is_published',
        )


class CatalogProductDetailSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(source='product.slug', read_only=True)
    title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = CatalogProductDetail
        fields = ('slug', 'title', 'content')


class PortfolioWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioWork
        fields = (
            'id',
            'title',
            'image_url',
            'alt_text',
            'sort_order',
            'is_published',
            'created_at',
        )
        read_only_fields = ('created_at',)


class GraphicModuleSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphicModuleSettings
        fields = (
            'banner_title',
            'banner_text',
            'module_title',
            'module_description',
            'max_upload_mb',
            'allowed_formats',
            'ink_limit_percent',
            'black_generation',
            'color_profile',
            'show_promo_banner',
            'disclaimer_text',
        )


class ChatBotTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotTemplate
        fields = ('id', 'key', 'text')


class ChatEscalateKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatEscalateKeyword
        fields = ('id', 'keyword', 'is_active')


class ChatFaqRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatFaqRule
        fields = ('id', 'pattern', 'reply', 'priority', 'is_active')


class QuoteServiceConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteServiceConfig
        fields = ('data', 'updated_at')


class StaffUserSerializer(serializers.ModelSerializer):
    is_administrator = serializers.BooleanField(required=False, default=False)
    is_manager = serializers.BooleanField(required=False, default=False)
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'email',
            'is_active',
            'is_administrator',
            'is_manager',
            'password',
        )
        read_only_fields = ('id',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['is_administrator'] = (
            instance.groups.filter(name=GROUP_ADMINISTRATOR).exists() or instance.is_superuser
        )
        data['is_manager'] = instance.groups.filter(name=GROUP_MANAGER).exists()
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        is_admin = validated_data.pop('is_administrator', False)
        is_manager = validated_data.pop('is_manager', False)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        self._set_roles(user, is_admin, is_manager)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        is_admin = validated_data.pop('is_administrator', None)
        is_manager = validated_data.pop('is_manager', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if is_admin is not None or is_manager is not None:
            self._set_roles(
                instance,
                is_admin if is_admin is not None else self.get_is_administrator(instance),
                is_manager if is_manager is not None else self.get_is_manager(instance),
            )
        return instance

    def _set_roles(self, user, is_admin: bool, is_manager: bool) -> None:
        admin_g, _ = Group.objects.get_or_create(name=GROUP_ADMINISTRATOR)
        mgr_g, _ = Group.objects.get_or_create(name=GROUP_MANAGER)
        user.groups.clear()
        if is_admin:
            user.groups.add(admin_g)
            user.is_staff = True
        elif is_manager:
            user.groups.add(mgr_g)
            user.is_staff = True
        user.save(update_fields=['is_staff'])
