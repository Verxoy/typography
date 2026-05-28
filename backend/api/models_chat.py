from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class ChatSession(models.Model):
    """Сессия чата на сайте (виджет → менеджер)."""

    class Status(models.TextChoices):
        BOT = 'bot', 'Бот'
        WAITING = 'waiting_manager', 'Ожидает менеджера'
        IN_PROGRESS = 'in_progress', 'В работе'
        CLOSED = 'closed', 'Закрыт'

    session_key = models.CharField(max_length=64, unique=True, db_index=True, verbose_name='Ключ сессии')
    public_number = models.CharField(max_length=32, unique=True, verbose_name='Номер чата')
    visitor_name = models.CharField(max_length=200, blank=True, default='', verbose_name='Имя')
    email = models.EmailField(blank=True, default='', verbose_name='Email')
    phone = models.CharField(max_length=32, blank=True, default='', verbose_name='Телефон')
    contact_submitted = models.BooleanField(default=False, verbose_name='Контакты отправлены')
    page_url = models.CharField(max_length=500, blank=True, default='', verbose_name='Страница')
    status = models.CharField(
        max_length=24,
        choices=Status.choices,
        default=Status.BOT,
        db_index=True,
        verbose_name='Статус',
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_chats',
        verbose_name='Менеджер',
    )
    manager_note = models.TextField(blank=True, default='', verbose_name='Заметка менеджера')
    escalated_at = models.DateTimeField(null=True, blank=True, verbose_name='Передан менеджеру')
    staff_visible_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name='В кабинете менеджера с',
    )

    bitrix_lead_id = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='ID лида в Битрикс')
    bitrix_synced_at = models.DateTimeField(null=True, blank=True, verbose_name='Отправлено в CRM')
    bitrix_sync_error = models.TextField(blank=True, default='', verbose_name='Ошибка CRM')
    bitrix_stub_path = models.CharField(max_length=500, blank=True, default='', verbose_name='Файл-заглушка CRM')

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-created_at']

    @property
    def request_type_label(self) -> str:
        return 'Чат'

    def __str__(self) -> str:
        return f'{self.public_number} — {self.get_status_display()}'

    @classmethod
    def new_session_key(cls) -> str:
        return uuid.uuid4().hex


class ChatMessage(models.Model):
    """Сообщение в чате."""

    class SenderType(models.TextChoices):
        VISITOR = 'visitor', 'Клиент'
        BOT = 'bot', 'Бот'
        MANAGER = 'manager', 'Менеджер'
        SYSTEM = 'system', 'Система'

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Сессия',
    )
    sender_type = models.CharField(max_length=16, choices=SenderType.choices, verbose_name='Отправитель')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'
        ordering = ['created_at']

    def __str__(self) -> str:
        return f'{self.session.public_number} [{self.sender_type}]'
