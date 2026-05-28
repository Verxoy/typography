import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage

CMS_UPLOAD_MAX_BYTES = 12 * 1024 * 1024
CMS_ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}


def save_cms_upload(uploaded_file, *, subdir: str = 'cms') -> str:
    """Сохраняет файл в MEDIA и возвращает URL вида /media/cms/…."""
    name = os.path.basename(uploaded_file.name or 'image').replace('..', '').strip()
    base, ext = os.path.splitext(name)
    ext = ext.lower()
    if ext not in CMS_ALLOWED_EXTENSIONS:
        raise ValueError(f'Недопустимый формат файла. Разрешены: {", ".join(sorted(CMS_ALLOWED_EXTENSIONS))}')
    if uploaded_file.size > CMS_UPLOAD_MAX_BYTES:
        raise ValueError('Файл слишком большой (максимум 12 МБ).')

    safe_base = ''.join(c for c in base if c.isalnum() or c in '-_')[:40] or 'image'
    filename = f'{safe_base}-{uuid.uuid4().hex[:10]}{ext}'
    rel_path = f'{subdir}/{filename}'
    saved = default_storage.save(rel_path, uploaded_file)
    media_url = settings.MEDIA_URL
    if not media_url.startswith('/'):
        media_url = '/' + media_url
    if not media_url.endswith('/'):
        media_url += '/'
    return f'{media_url}{saved}'
