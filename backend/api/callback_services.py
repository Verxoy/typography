"""Создание заявки на звонок и синхронизация с CRM."""
from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from .bitrix_sync import sync_callback_to_crm
from .models import CallbackRequest


def _next_public_number() -> str:
    year = timezone.now().year
    prefix = f'CB-{year}-'
    last = (
        CallbackRequest.objects.filter(public_number__startswith=prefix)
        .order_by('-id')
        .values_list('public_number', flat=True)
        .first()
    )
    if not last:
        return f'{prefix}0001'
    try:
        num = int(last.split('-')[-1]) + 1
    except ValueError:
        num = CallbackRequest.objects.count() + 1
    return f'{prefix}{num:04d}'


@transaction.atomic
def create_callback_request(*, name: str, phone: str) -> CallbackRequest:
    callback = CallbackRequest.objects.create(
        public_number=_next_public_number(),
        name=name.strip(),
        phone=phone.strip(),
    )
    try:
        lead_id, stub_path, sync_error = sync_callback_to_crm(callback)
        callback.bitrix_lead_id = lead_id
        callback.bitrix_stub_path = stub_path
        callback.bitrix_synced_at = timezone.now()
        callback.bitrix_sync_error = sync_error
        callback.save(
            update_fields=[
                'bitrix_lead_id',
                'bitrix_stub_path',
                'bitrix_synced_at',
                'bitrix_sync_error',
            ]
        )
    except Exception as exc:
        callback.bitrix_sync_error = str(exc)[:2000]
        callback.save(update_fields=['bitrix_sync_error'])
    return callback
