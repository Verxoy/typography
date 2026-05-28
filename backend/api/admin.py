from django.contrib import admin
from .models import CallbackRequest, ContactMessage, Resume
from .models_chat import ChatMessage, ChatSession
from .models_cms import (
    CatalogProduct,
    CatalogProductDetail,
    CatalogSection,
    ChatBotTemplate,
    ChatEscalateKeyword,
    ChatFaqRule,
    GraphicModuleSettings,
    QuoteServiceConfig,
)
from .models_quotes import QuoteAttachment, QuoteRequest


class QuoteAttachmentInline(admin.TabularInline):
    model = QuoteAttachment
    extra = 0
    readonly_fields = ('original_name', 'file_size', 'content_type', 'uploaded_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'phone', 'created_at', 'is_reviewed')
    list_filter = ('is_reviewed', 'created_at')
    search_fields = ('full_name', 'position', 'phone')


@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = (
        'public_number',
        'name',
        'phone',
        'site_status',
        'bitrix_lead_id',
        'created_at',
    )
    list_filter = ('site_status', 'created_at')
    search_fields = ('public_number', 'name', 'phone')
    readonly_fields = ('public_number', 'created_at', 'bitrix_synced_at', 'bitrix_stub_path')


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender_type', 'text', 'created_at')


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    inlines = [ChatMessageInline]
    list_display = (
        'public_number',
        'visitor_name',
        'email',
        'phone',
        'status',
        'assigned_to',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('public_number', 'visitor_name', 'phone', 'session_key')
    readonly_fields = (
        'public_number',
        'session_key',
        'created_at',
        'updated_at',
        'escalated_at',
        'bitrix_synced_at',
        'bitrix_stub_path',
    )


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    inlines = [QuoteAttachmentInline]
    list_display = (
        'public_number',
        'service_title',
        'company_name',
        'inn',
        'site_status',
        'bitrix_lead_id',
        'created_at',
    )
    list_filter = ('site_status', 'company_type', 'created_at')
    search_fields = ('public_number', 'company_name', 'inn', 'contact_phone', 'contact_email')
    readonly_fields = ('public_number', 'created_at', 'bitrix_synced_at', 'bitrix_stub_path')


@admin.register(CatalogSection)
class CatalogSectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'title', 'sort_order', 'is_published')


@admin.register(CatalogProduct)
class CatalogProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'slug', 'sort_order', 'is_published')
    list_filter = ('section',)
    search_fields = ('title', 'slug')


@admin.register(CatalogProductDetail)
class CatalogProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product',)
    search_fields = ('product__title', 'product__slug')


@admin.register(GraphicModuleSettings)
class GraphicModuleSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not GraphicModuleSettings.objects.exists()


@admin.register(ChatFaqRule)
class ChatFaqRuleAdmin(admin.ModelAdmin):
    list_display = ('pattern', 'priority', 'is_active')
    list_filter = ('is_active',)


@admin.register(ChatBotTemplate)
class ChatBotTemplateAdmin(admin.ModelAdmin):
    list_display = ('key',)


@admin.register(ChatEscalateKeyword)
class ChatEscalateKeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'is_active')


@admin.register(QuoteServiceConfig)
class QuoteServiceConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not QuoteServiceConfig.objects.exists()
