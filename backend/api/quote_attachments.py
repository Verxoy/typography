"""Валидация и сохранение макетов к заявке «Быстрый расчёт»."""
from __future__ import annotations

import os
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from .models_quotes import QuoteAttachment, QuoteRequest

ALLOWED_EXTENSIONS = frozenset({
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'pdf', 'ai', 'eps', 'cdr', 'zip', 'rar',
})

IMAGE_EXTENSIONS = frozenset({'jpg', 'jpeg', 'png', 'gif', 'webp'})

MAX_FILES = int(getattr(settings, 'QUOTE_MAX_ATTACHMENTS', 3))
MAX_FILE_SIZE = int(getattr(settings, 'QUOTE_MAX_FILE_SIZE', 25 * 1024 * 1024))


def _extension(filename: str) -> str:
    return Path(filename).suffix.lstrip('.').lower()


def validate_layout_files(files: list[UploadedFile]) -> None:
    if len(files) > MAX_FILES:
        raise ValidationError(f'Можно прикрепить не более {MAX_FILES} файлов.')
    for uploaded in files:
        name = uploaded.name or 'file'
        ext = _extension(name)
        if ext not in ALLOWED_EXTENSIONS:
            allowed = ', '.join(sorted(ALLOWED_EXTENSIONS))
            raise ValidationError(
                f'Файл «{name}»: недопустимый формат. Разрешены: {allowed}.'
            )
        size = uploaded.size or 0
        if size > MAX_FILE_SIZE:
            mb = MAX_FILE_SIZE // (1024 * 1024)
            raise ValidationError(f'Файл «{name}» слишком большой (максимум {mb} МБ).')


def save_quote_attachments(quote: QuoteRequest, files: list[UploadedFile]) -> list[QuoteAttachment]:
    if not files:
        return []
    validate_layout_files(files)
    saved: list[QuoteAttachment] = []
    for uploaded in files:
        att = QuoteAttachment(
            quote=quote,
            original_name=os.path.basename(uploaded.name or 'file'),
            content_type=(uploaded.content_type or '')[:120],
            file_size=uploaded.size or 0,
        )
        att.file.save(uploaded.name, uploaded, save=True)
        saved.append(att)
    return saved


def is_image_attachment(att: QuoteAttachment) -> bool:
    ext = _extension(att.original_name)
    if ext in IMAGE_EXTENSIONS:
        return True
    ct = (att.content_type or '').lower()
    return ct.startswith('image/')
