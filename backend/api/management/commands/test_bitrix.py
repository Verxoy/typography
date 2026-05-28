from django.conf import settings
from django.core.management.base import BaseCommand

from api.bitrix_client import BitrixApiError, _crm_entity, bitrix_call, validate_webhook_url


class Command(BaseCommand):
    help = 'Проверка подключения к Битрикс24 (входящий вебхук из .env)'

    def handle(self, *args, **options):
        url = getattr(settings, 'BITRIX_WEBHOOK_URL', '')
        entity = _crm_entity()
        method = 'crm.deal.add' if entity == 'deal' else 'crm.lead.add'
        where = 'CRM - Сделки' if entity == 'deal' else 'CRM - Лиды'

        self.stdout.write(f'BITRIX_ENABLED: {settings.BITRIX_ENABLED}')
        self.stdout.write(f'BITRIX_CRM_ENTITY: {entity} ({where})')

        err = validate_webhook_url(url)
        if err:
            self.stdout.write(self.style.ERROR(err))
            return

        host = url.split('/')[2] if '/' in url else url
        self.stdout.write(f'Портал: {host}')
        self.stdout.write(f'Вызов {method} (тест)…')

        fields = {'TITLE': 'Тест подключения сайта (можно удалить)', 'OPENED': 'Y'}
        if entity == 'deal':
            fields['COMMENTS'] = 'Проверка интеграции «Быстрый расчёт»'

        try:
            entity_id = bitrix_call(method, {'fields': fields})
        except BitrixApiError as exc:
            self.stdout.write(self.style.ERROR(f'Ошибка: {exc}'))
            return

        self.stdout.write(self.style.SUCCESS(f'OK — создано ID {entity_id}. Откройте {where}.'))
