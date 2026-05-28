"""Ссылки на раздел staff (для CRM и уведомлений)."""
from __future__ import annotations

from django.conf import settings

from .models_chat import ChatSession
from .models_quotes import QuoteRequest


def frontend_base_url() -> str:
    """Базовый URL фронтенда (Vue), не API Django."""
    base = getattr(settings, 'FRONTEND_BASE_URL', '') or 'http://127.0.0.1:5173'
    return str(base).rstrip('/')


def staff_quote_detail_url(quote: QuoteRequest) -> str:
    return f'{frontend_base_url()}/staff/quotes/{quote.public_number}'


def staff_chat_detail_url(session: ChatSession) -> str:
    return f'{frontend_base_url()}/staff/chats/{session.public_number}'
