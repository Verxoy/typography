"""Заглушка Битрикс24: запись лида в JSON-файл (этап разработки)."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from django.conf import settings

from .quote_catalog import quote_param_label

logger = logging.getLogger(__name__)


def build_lead_comments(quote) -> str:
    lines = [
        f'Номер заявки: {quote.public_number}',
        f'Услуга: {quote.service_title}',
        f'Заказчик: {quote.get_company_type_display()}'
        + (f' — {quote.company_name}' if quote.company_name else ''),
        f'ИНН: {quote.inn or "—"}',
        '--- Параметры ---',
    ]
    for key, val in (quote.parameters or {}).items():
        if val is None or str(val).strip() == '':
            continue
        lines.append(f'{quote_param_label(key, quote.service_slug)}: {val}')
    if quote.client_comment:
        lines.append(f'--- Комментарий ---\n{quote.client_comment}')
    attachments = list(quote.attachments.all())
    if attachments:
        lines.append('--- Макеты ---')
        lines.append('К заявке прикреплены макеты (файлы на сайте).')
        for att in attachments:
            lines.append(f'• {att.original_name} ({att.file_size // 1024} КБ)')
    return '\n'.join(lines)


def push_quote_lead_stub(quote) -> tuple[int | None, str]:
    """
    Имитирует crm.lead.add: пишет файл, возвращает (pseudo_lead_id, relative_path).
    """
    base = Path(getattr(settings, 'BITRIX_STUB_DIR', settings.BASE_DIR / 'data' / 'bitrix_stub'))
    base.mkdir(parents=True, exist_ok=True)

    pseudo_id = int(quote.pk) + 10000
    filename = f'quote_{quote.public_number}_{pseudo_id}.json'
    path = base / filename

    payload = {
        'stub': True,
        'method': 'crm.lead.add',
        'created_at': datetime.now().isoformat(),
        'lead_id_stub': pseudo_id,
        'fields': {
            'TITLE': f'Быстрый расчёт: {quote.service_title}',
            'NAME': quote.contact_name,
            'PHONE': quote.contact_phone,
            'EMAIL': quote.contact_email,
            'COMMENTS': build_lead_comments(quote),
            'SOURCE_ID': 'WEB',
        },
        'quote_request_id': quote.pk,
        'public_number': quote.public_number,
        'has_attachments': quote.attachments.exists(),
        'attachments': [
            {
                'original_name': att.original_name,
                'file_size': att.file_size,
                'content_type': att.content_type,
            }
            for att in quote.attachments.all()
        ],
    }

    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    rel = str(path.relative_to(settings.BASE_DIR))
    logger.info('Bitrix STUB: лид записан в %s', rel)
    return pseudo_id, rel


# Совместимость со старым именем
push_quote_lead = push_quote_lead_stub
