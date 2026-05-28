"""Отправка заявки в Битрикс24 (сделка или лид) через входящий вебхук."""
from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from typing import Any

from django.conf import settings

from .bitrix_stub import build_lead_comments

logger = logging.getLogger(__name__)


class BitrixApiError(Exception):
    """Ошибка вызова REST API Битрикс24."""


def validate_webhook_url(url: str) -> str | None:
    """Текст ошибки или None, если URL похож на входящий вебхук."""
    u = (url or '').strip().lower()
    if not u:
        return 'BITRIX_WEBHOOK_URL не задан в backend/.env'
    if '/devops/edit/in-hook' in u or '/devops/' in u:
        return (
            'Это ссылка на страницу настройки в Bitrix, а не вебхук. '
            'На той же странице скопируйте поле «Вебхук для вызова rest api» '
            '(адрес вида https://портал.bitrix24.ru/rest/1/код/).'
        )
    if '/rest/' not in u:
        return 'URL должен содержать /rest/ — скопируйте «Вебхук для вызова rest api» из Битрикс24'
    if 'profile' in u or 'user/' in u:
        return (
            'Похоже, скопирована ссылка на профиль, а не вебхук. '
            'Создайте: Приложения → Разработчикам → Входящий вебхук (право CRM).'
        )
    if 'profile.json' in u:
        return 'URL не должен содержать profile.json — нужен адрес вебхука со слэшем в конце'
    return None


def _webhook_base() -> str:
    url = (getattr(settings, 'BITRIX_WEBHOOK_URL', None) or '').strip()
    err = validate_webhook_url(url)
    if err:
        raise BitrixApiError(err)
    return url.rstrip('/') + '/'


def bitrix_call(method: str, params: dict[str, Any] | None = None) -> Any:
    url = _webhook_base() + method + '.json'
    body = json.dumps(params or {}, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=body,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode('utf-8')
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', errors='replace')
        raise BitrixApiError(f'HTTP {exc.code}: {detail[:500]}') from exc
    except urllib.error.URLError as exc:
        raise BitrixApiError(f'Сеть: {exc.reason}') from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BitrixApiError(f'Некорректный JSON: {raw[:200]}') from exc

    if 'error' in data:
        raise BitrixApiError(
            f"{data.get('error')}: {data.get('error_description', '')}".strip(': ')
        )
    return data.get('result')


def _crm_entity() -> str:
    """deal — сделки (канбан на скриншоте); lead — лиды."""
    mode = (getattr(settings, 'BITRIX_CRM_ENTITY', None) or 'deal').strip().lower()
    return mode if mode in ('deal', 'lead') else 'deal'


def _build_fields(quote) -> dict[str, Any]:
    comments = build_lead_comments(quote)
    contact_line = (
        f'Контакт: {quote.contact_name}, {quote.contact_phone}, {quote.contact_email}'
    )
    full_comments = f'{comments}\n\n{contact_line}'

    if _crm_entity() == 'lead':
        fields: dict[str, Any] = {
            'TITLE': f'Быстрый расчёт: {quote.service_title}',
            'NAME': quote.contact_name,
            'PHONE': [{'VALUE': quote.contact_phone, 'VALUE_TYPE': 'WORK'}],
            'EMAIL': [{'VALUE': quote.contact_email, 'VALUE_TYPE': 'WORK'}],
            'COMMENTS': full_comments,
            'SOURCE_ID': 'WEB',
        }
        if quote.company_name.strip():
            fields['COMPANY_TITLE'] = quote.company_name.strip()
        return fields

    # Сделка — попадает в CRM → Сделки (колонка «Новая» в общей воронке)
    title = f'Быстрый расчёт: {quote.service_title} — {quote.company_name}'
    fields = {
        'TITLE': title[:255],
        'COMMENTS': full_comments,
        'OPENED': 'Y',
        'SOURCE_ID': 'WEB',
        'SOURCE_DESCRIPTION': quote.public_number,
    }
    category_id = getattr(settings, 'BITRIX_DEAL_CATEGORY_ID', None)
    if category_id is not None and str(category_id).strip() != '':
        fields['CATEGORY_ID'] = int(category_id)
    return fields


def push_quote_to_bitrix(quote) -> int:
    """Создаёт сделку или лид в CRM, возвращает ID."""
    entity = _crm_entity()
    method = 'crm.deal.add' if entity == 'deal' else 'crm.lead.add'
    fields = _build_fields(quote)

    entity_id = bitrix_call(method, {'fields': fields})
    if entity_id is None:
        raise BitrixApiError(f'{method} не вернул ID')

    label = 'сделка' if entity == 'deal' else 'лид'
    logger.info('Bitrix24: создана %s %s для заявки %s', label, entity_id, quote.public_number)
    return int(entity_id)


# Совместимость
push_quote_lead_bitrix = push_quote_to_bitrix
