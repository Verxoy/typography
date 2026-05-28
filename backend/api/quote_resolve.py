"""Поиск заявки по публичному номеру (QR-…) или устаревшему числовому id."""
from __future__ import annotations

from .models import CallbackRequest
from .models_chat import ChatSession
from .models_quotes import QuoteRequest


def get_quote_by_ref(ref: str) -> QuoteRequest:
    ref = (ref or '').strip()
    if not ref:
        raise QuoteRequest.DoesNotExist

    if ref.isdigit():
        try:
            return QuoteRequest.objects.get(pk=int(ref))
        except QuoteRequest.DoesNotExist:
            pass

    return QuoteRequest.objects.get(public_number=ref)


def get_callback_by_ref(ref: str) -> CallbackRequest:
    ref = (ref or '').strip()
    if not ref:
        raise CallbackRequest.DoesNotExist

    if ref.isdigit():
        try:
            return CallbackRequest.objects.get(pk=int(ref))
        except CallbackRequest.DoesNotExist:
            pass

    return CallbackRequest.objects.get(public_number=ref)


def get_chat_by_ref(ref: str) -> ChatSession:
    ref = (ref or '').strip()
    if not ref:
        raise ChatSession.DoesNotExist

    if ref.isdigit():
        try:
            return ChatSession.objects.get(pk=int(ref))
        except ChatSession.DoesNotExist:
            pass

    return ChatSession.objects.get(public_number=ref)
