"""Маршрутизация: Битрикс24 или файловая заглушка."""
from __future__ import annotations

import logging

from django.conf import settings

from .bitrix_callback import push_callback_lead_stub, push_callback_to_bitrix
from .bitrix_chat import push_chat_lead_stub, push_chat_to_bitrix
from .bitrix_client import BitrixApiError, push_quote_to_bitrix
from .bitrix_stub import push_quote_lead_stub

logger = logging.getLogger(__name__)


def sync_quote_to_crm(quote) -> tuple[int | None, str, str]:
    """
    Возвращает (lead_id, stub_path, sync_error).
    sync_error пустая строка при успехе в Bitrix; при fallback после ошибки — текст ошибки Bitrix.
    """
    if getattr(settings, 'BITRIX_ENABLED', False) and getattr(settings, 'BITRIX_WEBHOOK_URL', ''):
        try:
            lead_id = push_quote_to_bitrix(quote)
            return lead_id, '', ''
        except BitrixApiError as exc:
            logger.warning('Bitrix24: %s', exc)
            if getattr(settings, 'BITRIX_STUB_FALLBACK', True):
                lead_id, stub_path = push_quote_lead_stub(quote)
                return lead_id, stub_path, str(exc)[:2000]
            raise

    lead_id, stub_path = push_quote_lead_stub(quote)
    return lead_id, stub_path, ''


def sync_callback_to_crm(callback) -> tuple[int | None, str, str]:
    """Заявка на звонок всегда уходит в CRM как лид."""
    if getattr(settings, 'BITRIX_ENABLED', False) and getattr(settings, 'BITRIX_WEBHOOK_URL', ''):
        try:
            lead_id = push_callback_to_bitrix(callback)
            return lead_id, '', ''
        except BitrixApiError as exc:
            logger.warning('Bitrix24 (звонок): %s', exc)
            if getattr(settings, 'BITRIX_STUB_FALLBACK', True):
                lead_id, stub_path = push_callback_lead_stub(callback)
                return lead_id, stub_path, str(exc)[:2000]
            raise

    lead_id, stub_path = push_callback_lead_stub(callback)
    return lead_id, stub_path, ''


def sync_chat_to_crm(session) -> tuple[int | None, str, str]:
    """Лид из чата после отправки контактов клиентом."""
    if getattr(settings, 'BITRIX_ENABLED', False) and getattr(settings, 'BITRIX_WEBHOOK_URL', ''):
        try:
            lead_id = push_chat_to_bitrix(session)
            return lead_id, '', ''
        except BitrixApiError as exc:
            logger.warning('Bitrix24 (чат): %s', exc)
            if getattr(settings, 'BITRIX_STUB_FALLBACK', True):
                lead_id, stub_path = push_chat_lead_stub(session)
                return lead_id, stub_path, str(exc)[:2000]
            raise

    lead_id, stub_path = push_chat_lead_stub(session)
    return lead_id, stub_path, ''
