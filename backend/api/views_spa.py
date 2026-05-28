"""Раздача собранного Vue (vue-project/dist) с Django — один порт для CRM-ссылок."""
from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse

VUE_DIST = Path(settings.BASE_DIR).parent / 'vue-project' / 'dist'
VUE_INDEX = VUE_DIST / 'index.html'
VUE_ASSETS = VUE_DIST / 'assets'


def _spa_not_built_response() -> HttpResponse:
    return HttpResponse(
        'Сайт не собран. Выполните: cd vue-project && npm run build',
        status=503,
        content_type='text/plain; charset=utf-8',
    )


class SpaAssetView:
    """Callable for path('assets/<path:path>', ...)."""

    def __call__(self, request, path: str):
        if not VUE_ASSETS.is_dir():
            return _spa_not_built_response()
        file_path = (VUE_ASSETS / path).resolve()
        assets_root = VUE_ASSETS.resolve()
        if not str(file_path).startswith(str(assets_root)) or not file_path.is_file():
            raise Http404
        return FileResponse(file_path.open('rb'))


class SpaStaffView:
    """Vue Router history: любой /staff/… → index.html."""

    def __call__(self, request, path: str = ''):
        if not VUE_INDEX.is_file():
            return _spa_not_built_response()
        return FileResponse(VUE_INDEX.open('rb'), content_type='text/html; charset=utf-8')
