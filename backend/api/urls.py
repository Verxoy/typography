from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContactMessageViewSet,
    ResumeViewSet,
    CallbackRequestViewSet,
    send_contact_message,
    send_resume,
    request_callback,
)
from .views_auth import auth_csrf, auth_login, auth_logout, auth_me
from .views_quotes import QuoteCatalogView, quote_submit
from .views_chat import (
    ChatContactSubmitView,
    ChatEscalateView,
    ChatMessageListView,
    ChatSendMessageView,
    ChatSessionCreateView,
)
from .views_staff_callbacks import StaffCallbackDetailView, StaffCallbackListView
from .views_staff_chat import StaffChatDetailView, StaffChatListView, StaffChatReplyView
from .views_staff_inbox import StaffInboxListView
from .views_catalog import PublicCatalogProductDetailView, PublicCatalogView
from .views_portfolio import PublicPortfolioView
from .views_graphic_public import PublicGraphicSettingsView
from .views_staff_cms import (
    StaffCatalogProductDetailView,
    StaffCatalogProductListView,
    StaffCatalogProductPageView,
    StaffCatalogSectionDetailView,
    StaffCatalogSectionListView,
    StaffChatFaqDetailView,
    StaffChatFaqListView,
    StaffChatKeywordsView,
    StaffChatTemplatesView,
    StaffCmsMediaUploadView,
    StaffGraphicSettingsView,
    StaffPortfolioDetailView,
    StaffPortfolioListView,
    StaffQuoteCatalogView,
    StaffUserDetailView,
    StaffUserListView,
)
from .views_staff_quotes import (
    StaffQuoteAttachmentView,
    StaffQuoteDetailView,
    StaffQuoteListView,
)

router = DefaultRouter()
router.register(r'contacts', ContactMessageViewSet, basename='contact')
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'callbacks', CallbackRequestViewSet, basename='callback')

urlpatterns = [
    path('', include(router.urls)),
    path('send-message/', send_contact_message, name='send-message'),
    path('send-resume/', send_resume, name='send-resume'),
    path('request-callback/', request_callback, name='request-callback'),
    path('chat/session/', ChatSessionCreateView.as_view(), name='chat-session-create'),
    path('chat/session/<str:session_key>/messages/', ChatMessageListView.as_view(), name='chat-messages'),
    path('chat/session/<str:session_key>/send/', ChatSendMessageView.as_view(), name='chat-send'),
    path('chat/session/<str:session_key>/escalate/', ChatEscalateView.as_view(), name='chat-escalate'),
    path('chat/session/<str:session_key>/contact/', ChatContactSubmitView.as_view(), name='chat-contact'),
    path('catalog/', PublicCatalogView.as_view(), name='public-catalog'),
    path(
        'catalog/products/<slug:slug>/',
        PublicCatalogProductDetailView.as_view(),
        name='public-catalog-product',
    ),
    path('graphic-module/settings/', PublicGraphicSettingsView.as_view(), name='graphic-settings'),
    path('portfolio/', PublicPortfolioView.as_view(), name='public-portfolio'),
    path('quotes/catalog/', QuoteCatalogView.as_view(), name='quote-catalog'),
    path('quotes/submit/', quote_submit, name='quote-submit'),
    path('auth/csrf/', auth_csrf, name='auth-csrf'),
    path('auth/login/', auth_login, name='auth-login'),
    path('auth/logout/', auth_logout, name='auth-logout'),
    path('auth/me/', auth_me, name='auth-me'),
    path('staff/inbox/', StaffInboxListView.as_view(), name='staff-inbox'),
    path('staff/quotes/', StaffQuoteListView.as_view(), name='staff-quotes'),
    path('staff/quotes/<str:ref>/', StaffQuoteDetailView.as_view(), name='staff-quote-detail'),
    path('staff/callbacks/', StaffCallbackListView.as_view(), name='staff-callbacks'),
    path('staff/callbacks/<str:ref>/', StaffCallbackDetailView.as_view(), name='staff-callback-detail'),
    path('staff/chats/', StaffChatListView.as_view(), name='staff-chats'),
    path('staff/chats/<str:ref>/', StaffChatDetailView.as_view(), name='staff-chat-detail'),
    path('staff/chats/<str:ref>/reply/', StaffChatReplyView.as_view(), name='staff-chat-reply'),
    path(
        'staff/quotes/<str:ref>/attachments/<int:attachment_id>/',
        StaffQuoteAttachmentView.as_view(),
        name='staff-quote-attachment',
    ),
    path('staff/cms/catalog/sections/', StaffCatalogSectionListView.as_view()),
    path('staff/cms/catalog/sections/<int:pk>/', StaffCatalogSectionDetailView.as_view()),
    path('staff/cms/catalog/products/', StaffCatalogProductListView.as_view()),
    path('staff/cms/catalog/products/<int:pk>/', StaffCatalogProductDetailView.as_view()),
    path('staff/cms/catalog/pages/<slug:slug>/', StaffCatalogProductPageView.as_view()),
    path('staff/cms/upload/', StaffCmsMediaUploadView.as_view()),
    path('staff/cms/portfolio/', StaffPortfolioListView.as_view()),
    path('staff/cms/portfolio/<int:pk>/', StaffPortfolioDetailView.as_view()),
    path('staff/cms/graphic/', StaffGraphicSettingsView.as_view()),
    path('staff/cms/chat/faq/', StaffChatFaqListView.as_view()),
    path('staff/cms/chat/faq/<int:pk>/', StaffChatFaqDetailView.as_view()),
    path('staff/cms/chat/templates/', StaffChatTemplatesView.as_view()),
    path('staff/cms/chat/keywords/', StaffChatKeywordsView.as_view()),
    path('staff/cms/quotes/', StaffQuoteCatalogView.as_view()),
    path('staff/cms/users/', StaffUserListView.as_view()),
    path('staff/cms/users/<int:pk>/', StaffUserDetailView.as_view()),
]
