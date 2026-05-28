from django.db import models

from .models_quotes import QuoteRequest  # noqa: F401


class ContactMessage(models.Model):
    """Сообщения из формы контактов"""
    name = models.CharField(max_length=200, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_processed = models.BooleanField(default=False, verbose_name='Обработано')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.email}'


class Resume(models.Model):
    """Резюме соискателей"""
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    age = models.IntegerField(verbose_name='Возраст')
    education = models.CharField(max_length=300, verbose_name='Образование')
    position = models.CharField(max_length=200, verbose_name='Желаемая должность')
    salary = models.CharField(max_length=50, verbose_name='Желаемая зарплата')
    experience = models.CharField(max_length=100, verbose_name='Опыт работы')
    phone = models.CharField(max_length=20, verbose_name='Телефон WhatsApp')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    is_reviewed = models.BooleanField(default=False, verbose_name='Просмотрено')

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.position}'


class CallbackRequest(models.Model):
    """Заявка «Заказать звонок» с главной страницы сайта."""

    class SiteStatus(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_REVIEW = 'in_review', 'В работе'
        CLOSED = 'closed', 'Перезвонили'

    public_number = models.CharField(max_length=32, unique=True, verbose_name='Номер заявки')
    name = models.CharField(max_length=200, verbose_name='Имя')
    phone = models.CharField(max_length=32, verbose_name='Телефон')
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
    is_called = models.BooleanField(default=False, verbose_name='Перезвонили (устар.)')

    class Meta:
        verbose_name = 'Заявка на звонок'
        verbose_name_plural = 'Заявки на звонок'
        ordering = ['-created_at']

    @property
    def request_type_label(self) -> str:
        return 'Заказ звонка'

    def __str__(self):
        return f'{self.public_number} — {self.name}'
