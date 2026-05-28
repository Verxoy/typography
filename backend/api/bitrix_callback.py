"""Отправка заявки «Заказ звонка» в Битрикс24 (всегда лид)."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from django.conf import settings

from .bitrix_client import BitrixApiError, bitrix_call
from .models import CallbackRequest

logger = logging.getLogger(__name__)


def build_callback_lead_comments(callback: CallbackRequest) -> str:
    return '\n'.join(
        [
            'Тип заявки: заказ обратного звонка с сайта (не «Быстрый расчёт»).',
            f'Номер заявки: {callback.public_number}',
            f'Имя: {callback.name}',
            f'Телефон для звонка: {callback.phone}',
            '',
            'Клиент оставил контакты в форме «Заказать звонок» на главной странице.',
        ]
    )


def _callback_lead_fields(callback: CallbackRequest) -> dict:
    return {
        'TITLE': f'Заказ звонка: {callback.name}',
        'NAME': callback.name,
        'PHONE': [{'VALUE': callback.phone, 'VALUE_TYPE': 'WORK'}],
        'COMMENTS': build_callback_lead_comments(callback),
        'SOURCE_ID': 'WEB',
        'SOURCE_DESCRIPTION': f'Заказ звонка {callback.public_number}',
    }


def push_callback_to_bitrix(callback: CallbackRequest) -> int:
    entity_id = bitrix_call('crm.lead.add', {'fields': _callback_lead_fields(callback)})
    if entity_id is None:
        raise BitrixApiError('crm.lead.add не вернул ID')
    logger.info('Bitrix24: создан лид %s для заявки на звонок %s', entity_id, callback.public_number)
    return int(entity_id)


def push_callback_lead_stub(callback: CallbackRequest) -> tuple[int | None, str]:
    base = Path(getattr(settings, 'BITRIX_STUB_DIR', settings.BASE_DIR / 'data' / 'bitrix_stub'))
    base.mkdir(parents=True, exist_ok=True)

    pseudo_id = int(callback.pk) + 20000
    filename = f'callback_{callback.public_number}_{pseudo_id}.json'
    path = base / filename

    payload = {
        'stub': True,
        'method': 'crm.lead.add',
        'request_type': 'callback',
        'created_at': datetime.now().isoformat(),
        'lead_id_stub': pseudo_id,
        'fields': _callback_lead_fields(callback),
        'callback_request_id': callback.pk,
        'public_number': callback.public_number,
    }

    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    rel = str(path.relative_to(settings.BASE_DIR))
    logger.info('Bitrix STUB: лид (звонок) записан в %s', rel)
    return pseudo_id, rel
