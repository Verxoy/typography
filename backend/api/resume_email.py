"""Отправка анкеты резюме на почту типографии."""
from __future__ import annotations

import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Resume

logger = logging.getLogger(__name__)


def _format_resume_body(resume: Resume) -> str:
    sent_at = timezone.localtime(resume.created_at).strftime('%d.%m.%Y %H:%M')
    return (
        'Новая анкета «Отправить резюме» с сайта типографии.\n\n'
        f'ФИО: {resume.full_name}\n'
        f'Возраст: {resume.age}\n'
        f'Желаемая должность: {resume.position}\n'
        f'Желаемая зарплата: {resume.salary}\n'
        f'Образование: {resume.education}\n'
        f'Опыт работы в типографии: {resume.experience}\n'
        f'Телефон (WhatsApp): {resume.phone}\n\n'
        f'Дата отправки: {sent_at}\n'
    )


def send_resume_notification(resume: Resume) -> None:
    recipient = settings.RESUME_NOTIFY_EMAIL
    if not recipient:
        raise ValueError('RESUME_NOTIFY_EMAIL не задан')

    subject = f'Резюме с сайта: {resume.full_name} — {resume.position}'
    body = _format_resume_body(resume)
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        sent = send_mail(
            subject,
            body,
            from_email,
            [recipient],
            fail_silently=False,
        )
    except Exception as exc:
        raise RuntimeError(f'Ошибка SMTP: {exc}') from exc

    if sent != 1:
        raise RuntimeError('Письмо не было отправлено')

    if getattr(settings, 'RESUME_EMAIL_USE_SMTP', False):
        logger.info('Резюме %s отправлено на %s', resume.pk, recipient)
    else:
        logger.info(
            'Резюме %s сохранено в %s (SMTP не настроен)',
            resume.pk,
            getattr(settings, 'EMAIL_FILE_PATH', 'outbox'),
        )
