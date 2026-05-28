"""Отправка лида из чата на сайте в Битрикс24."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from django.conf import settings

from .bitrix_client import BitrixApiError, bitrix_call
from .models_chat import ChatMessage, ChatSession
from .quote_links import staff_chat_detail_url

logger = logging.getLogger(__name__)


def _chat_transcript_excerpt(session: ChatSession, limit: int = 12) -> str:
    lines: list[str] = []
    for msg in session.messages.order_by('created_at')[:limit]:
        label = {
            ChatMessage.SenderType.VISITOR: 'Клиент',
            ChatMessage.SenderType.BOT: 'Бот',
            ChatMessage.SenderType.MANAGER: 'Менеджер',
            ChatMessage.SenderType.SYSTEM: 'Система',
        }.get(msg.sender_type, msg.sender_type)
        text = (msg.text or '').replace('\n', ' ').strip()
        if text:
            lines.append(f'{label}: {text}')
    return '\n'.join(lines)


def build_chat_lead_comments(session: ChatSession) -> str:
    parts = [
        'Тип заявки: чат на сайте (виджет поддержки).',
        f'Номер чата: {session.public_number}',
        f'Имя: {session.visitor_name}',
        f'Email: {session.email}',
        f'Телефон: {session.phone}',
    ]
    if session.page_url:
        parts.append(f'Страница: {session.page_url}')
    parts.append(f'Карточка на сайте: {staff_chat_detail_url(session)}')
    transcript = _chat_transcript_excerpt(session)
    if transcript:
        parts.extend(['', '--- Переписка ---', transcript])
    return '\n'.join(parts)


def _chat_lead_fields(session: ChatSession) -> dict:
    title_name = session.visitor_name or 'Клиент'
    return {
        'TITLE': f'Чат с сайта: {title_name}',
        'NAME': session.visitor_name,
        'EMAIL': [{'VALUE': session.email, 'VALUE_TYPE': 'WORK'}] if session.email else [],
        'PHONE': [{'VALUE': session.phone, 'VALUE_TYPE': 'WORK'}] if session.phone else [],
        'COMMENTS': build_chat_lead_comments(session),
        'SOURCE_ID': 'WEB',
        'SOURCE_DESCRIPTION': f'Чат {session.public_number}',
    }


def push_chat_to_bitrix(session: ChatSession) -> int:
    entity_id = bitrix_call('crm.lead.add', {'fields': _chat_lead_fields(session)})
    if entity_id is None:
        raise BitrixApiError('crm.lead.add не вернул ID')
    logger.info('Bitrix24: создан лид %s для чата %s', entity_id, session.public_number)
    return int(entity_id)


def push_chat_lead_stub(session: ChatSession) -> tuple[int | None, str]:
    base = Path(getattr(settings, 'BITRIX_STUB_DIR', settings.BASE_DIR / 'data' / 'bitrix_stub'))
    base.mkdir(parents=True, exist_ok=True)

    pseudo_id = int(session.pk) + 30000
    filename = f'chat_{session.public_number}_{pseudo_id}.json'
    path = base / filename

    payload = {
        'stub': True,
        'method': 'crm.lead.add',
        'request_type': 'chat',
        'created_at': datetime.now().isoformat(),
        'lead_id_stub': pseudo_id,
        'fields': _chat_lead_fields(session),
        'chat_session_id': session.pk,
        'public_number': session.public_number,
    }

    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    rel = str(path.relative_to(settings.BASE_DIR))
    logger.info('Bitrix STUB: лид (чат) записан в %s', rel)
    return pseudo_id, rel
