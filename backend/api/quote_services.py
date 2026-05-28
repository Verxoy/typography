"""Создание заявки и синхронизация с CRM (заглушка)."""
from __future__ import annotations

from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.utils import timezone

from .bitrix_sync import sync_quote_to_crm
from .models_quotes import QuoteRequest
from .quote_attachments import save_quote_attachments


def _next_public_number() -> str:
    year = timezone.now().year
    prefix = f'QR-{year}-'
    last = (
        QuoteRequest.objects.filter(public_number__startswith=prefix)
        .order_by('-id')
        .values_list('public_number', flat=True)
        .first()
    )
    if not last:
        return f'{prefix}0001'
    try:
        num = int(last.split('-')[-1]) + 1
    except ValueError:
        num = QuoteRequest.objects.count() + 1
    return f'{prefix}{num:04d}'


@transaction.atomic
def create_quote_request(
    *,
    layout_files: list[UploadedFile] | None = None,
    **data,
) -> QuoteRequest:
    quote = QuoteRequest.objects.create(
        public_number=_next_public_number(),
        **data,
    )
    save_quote_attachments(quote, layout_files or [])
    try:
        lead_id, stub_path, sync_error = sync_quote_to_crm(quote)
        quote.bitrix_lead_id = lead_id
        quote.bitrix_stub_path = stub_path
        quote.bitrix_synced_at = timezone.now()
        quote.bitrix_sync_error = sync_error
        quote.save(
            update_fields=[
                'bitrix_lead_id',
                'bitrix_stub_path',
                'bitrix_synced_at',
                'bitrix_sync_error',
            ]
        )
    except Exception as exc:
        quote.bitrix_sync_error = str(exc)[:2000]
        quote.save(update_fields=['bitrix_sync_error'])
    return quote
