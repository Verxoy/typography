import os

from django.db import models


def quote_attachment_upload_to(instance, filename: str) -> str:
    number = instance.quote.public_number if instance.quote_id else 'draft'
    safe_name = os.path.basename(filename).replace('..', '').strip() or 'file'
    return f'quotes/{number}/{safe_name}'


class QuoteRequest(models.Model):
    """Заявка «Быстрый расчёт» — структурированная спецификация для КП."""

    class CompanyType(models.TextChoices):
        IP = 'ip', 'ИП'
        OOO = 'ooo', 'ООО'
        PRIVATE = 'private', 'Частный заказ'

    class SiteStatus(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_REVIEW = 'in_review', 'В работе'
        KP_SENT = 'kp_sent', 'Коммерческое предложение отправлено'
        CLOSED = 'closed', 'Закрыта'

    public_number = models.CharField(max_length=32, unique=True, verbose_name='Номер заявки')
    service_slug = models.CharField(max_length=64, verbose_name='Код услуги')
    service_title = models.CharField(max_length=200, verbose_name='Услуга')
    parameters = models.JSONField(default=dict, verbose_name='Параметры заказа')

    company_type = models.CharField(max_length=8, choices=CompanyType.choices, verbose_name='Тип юрлица')
    company_name = models.CharField(
        max_length=300, blank=True, default='', verbose_name='Название организации'
    )
    inn = models.CharField(max_length=12, blank=True, default='', db_index=True, verbose_name='ИНН')

    contact_name = models.CharField(max_length=200, verbose_name='Контактное лицо')
    contact_phone = models.CharField(max_length=32, verbose_name='Телефон')
    contact_email = models.EmailField(verbose_name='Email')
    client_comment = models.TextField(blank=True, default='', verbose_name='Комментарий клиента')

    site_status = models.CharField(
        max_length=20,
        choices=SiteStatus.choices,
        default=SiteStatus.NEW,
        verbose_name='Статус на сайте',
    )
    manager_note = models.TextField(blank=True, default='', verbose_name='Заметка менеджера')

    bitrix_lead_id = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='ID лида в Битрикс')
    bitrix_synced_at = models.DateTimeField(null=True, blank=True, verbose_name='Отправлено в CRM')
    bitrix_sync_error = models.TextField(blank=True, default='', verbose_name='Ошибка CRM')
    bitrix_stub_path = models.CharField(max_length=500, blank=True, default='', verbose_name='Файл-заглушка CRM')

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Заявка на расчёт'
        verbose_name_plural = 'Заявки на расчёт'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.public_number} — {self.service_title}'


class QuoteAttachment(models.Model):
    """Макет или вложение к заявке «Быстрый расчёт»."""

    quote = models.ForeignKey(
        QuoteRequest,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='Заявка',
    )
    file = models.FileField(upload_to=quote_attachment_upload_to, verbose_name='Файл')
    original_name = models.CharField(max_length=255, verbose_name='Имя файла')
    content_type = models.CharField(max_length=120, blank=True, default='', verbose_name='MIME')
    file_size = models.PositiveIntegerField(default=0, verbose_name='Размер (байт)')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вложение к заявке'
        verbose_name_plural = 'Вложения к заявкам'
        ordering = ['id']

    def __str__(self):
        return self.original_name
