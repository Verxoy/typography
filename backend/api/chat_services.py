"""Создание сессий, сообщений и эскалация чата."""
from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.utils import timezone

from .chat_bot import bot_reply, get_template_text
from .bitrix_sync import sync_chat_to_crm
from .models_chat import ChatMessage, ChatSession


def _next_public_number() -> str:
    year = timezone.now().year
    prefix = f'CH-{year}-'
    last = (
        ChatSession.objects.filter(public_number__startswith=prefix)
        .order_by('-id')
        .values_list('public_number', flat=True)
        .first()
    )
    if not last:
        return f'{prefix}0001'
    try:
        num = int(last.split('-')[-1]) + 1
    except ValueError:
        num = ChatSession.objects.count() + 1
    return f'{prefix}{num:04d}'


def session_needs_contact_form(session: ChatSession) -> bool:
    """Контакты ещё не отправлены, диалог передан менеджеру (в т.ч. после его ответа)."""
    return not session.contact_submitted and session.status in (
        ChatSession.Status.WAITING,
        ChatSession.Status.IN_PROGRESS,
    )


def staff_inbox_chat_queryset():
    """Чаты, которые показываем менеджеру (не пустые открытия виджета)."""
    return ChatSession.objects.filter(staff_visible_at__isnull=False)


def mark_staff_visible(session: ChatSession) -> None:
    if session.staff_visible_at:
        return
    now = timezone.now()
    ChatSession.objects.filter(pk=session.pk, staff_visible_at__isnull=True).update(
        staff_visible_at=now,
        updated_at=now,
    )
    session.staff_visible_at = now


def add_message(
    session: ChatSession,
    *,
    sender_type: str,
    text: str,
) -> ChatMessage:
    msg = ChatMessage.objects.create(
        session=session,
        sender_type=sender_type,
        text=text.strip(),
    )
    ChatSession.objects.filter(pk=session.pk).update(updated_at=timezone.now())
    return msg


@transaction.atomic
def get_or_create_session(*, session_key: str | None = None, page_url: str = '') -> ChatSession:
    key = (session_key or '').strip()
    if key:
        session = ChatSession.objects.filter(session_key=key).first()
        if session:
            if page_url and not session.page_url:
                session.page_url = page_url[:500]
                session.save(update_fields=['page_url', 'updated_at'])
            return session

    session = ChatSession.objects.create(
        session_key=key or ChatSession.new_session_key(),
        public_number=_next_public_number(),
        page_url=(page_url or '')[:500],
        status=ChatSession.Status.BOT,
    )
    add_message(session, sender_type=ChatMessage.SenderType.BOT, text=get_template_text('welcome'))
    return session


@transaction.atomic
def handle_visitor_message(session: ChatSession, text: str) -> list[ChatMessage]:
    """Сохраняет сообщение клиента и при необходимости отвечает ботом."""
    text = (text or '').strip()
    if not text:
        return list(session.messages.order_by('created_at'))

    created: list[ChatMessage] = []
    created.append(
        add_message(session, sender_type=ChatMessage.SenderType.VISITOR, text=text)
    )
    mark_staff_visible(session)

    if session.status == ChatSession.Status.CLOSED:
        created.append(
            add_message(
                session,
                sender_type=ChatMessage.SenderType.SYSTEM,
                text='Чат закрыт. Напишите «менеджер», чтобы открыть новый диалог — мы передадим обращение снова.',
            )
        )
        return created

    if session.status in (ChatSession.Status.WAITING, ChatSession.Status.IN_PROGRESS):
        return created

    turn = bot_reply(text, already_waiting=False)

    if turn.should_escalate:
        escalate_session(session)
        session.refresh_from_db()
        return list(session.messages.order_by('created_at'))

    if turn.reply:
        created.append(add_message(session, sender_type=ChatMessage.SenderType.BOT, text=turn.reply))
    return created


@transaction.atomic
def normalize_phone(phone: str) -> str:
    digits = re.sub(r'\D', '', phone or '')
    if digits.startswith('8') and len(digits) >= 11:
        digits = '7' + digits[1:]
    elif digits and not digits.startswith('7'):
        digits = '7' + digits
    if len(digits) < 11:
        raise ValidationError('Укажите номер телефона полностью (после +7).')
    return f'+{digits[:11]}'


def escalate_session(
    session: ChatSession,
    *,
    name: str = '',
    phone: str = '',
) -> ChatSession:
    if name:
        session.visitor_name = name.strip()[:200]
    if phone:
        session.phone = normalize_phone(phone)
    if session.status in (ChatSession.Status.BOT, ChatSession.Status.CLOSED):
        session.status = ChatSession.Status.WAITING
    if not session.escalated_at:
        session.escalated_at = timezone.now()
    session.save()

    escalate_confirm = get_template_text('escalate_confirm')
    if session.messages.filter(sender_type=ChatMessage.SenderType.SYSTEM, text=escalate_confirm).exists():
        return session

    add_message(session, sender_type=ChatMessage.SenderType.SYSTEM, text=escalate_confirm)
    return session


@transaction.atomic
def submit_contact(
    session: ChatSession,
    *,
    name: str,
    email: str,
    phone: str,
) -> ChatSession:
    name = (name or '').strip()[:200]
    email = (email or '').strip().lower()
    if not name:
        raise ValidationError('Укажите имя.')
    try:
        validate_email(email)
    except ValidationError as exc:
        raise ValidationError('Укажите корректный email.') from exc

    session.visitor_name = name
    session.email = email
    session.phone = normalize_phone(phone)
    session.contact_submitted = True
    mark_staff_visible(session)
    if session.status == ChatSession.Status.BOT:
        session.status = ChatSession.Status.WAITING
    if not session.escalated_at:
        session.escalated_at = timezone.now()
    session.save()

    if not session.bitrix_lead_id and not session.bitrix_synced_at:
        try:
            lead_id, stub_path, sync_error = sync_chat_to_crm(session)
            session.bitrix_lead_id = lead_id
            session.bitrix_stub_path = stub_path
            session.bitrix_synced_at = timezone.now()
            session.bitrix_sync_error = sync_error
            session.save(
                update_fields=[
                    'bitrix_lead_id',
                    'bitrix_stub_path',
                    'bitrix_synced_at',
                    'bitrix_sync_error',
                ]
            )
        except Exception as exc:
            session.bitrix_sync_error = str(exc)[:2000]
            session.save(update_fields=['bitrix_sync_error'])

    add_message(session, sender_type=ChatMessage.SenderType.SYSTEM, text=get_template_text('contact_thanks'))
    return session


@transaction.atomic
def assign_manager(session: ChatSession, user) -> ChatSession:
    session.assigned_to = user
    if session.status == ChatSession.Status.WAITING:
        session.status = ChatSession.Status.IN_PROGRESS
    session.save(update_fields=['assigned_to', 'status', 'updated_at'])

    if not session.messages.filter(
        sender_type=ChatMessage.SenderType.SYSTEM, text=get_template_text('manager_joined')
    ).exists():
        add_message(session, sender_type=ChatMessage.SenderType.SYSTEM, text=get_template_text('manager_joined'))
    return session


@transaction.atomic
def manager_reply(session: ChatSession, user, text: str) -> ChatMessage:
    if session.status == ChatSession.Status.WAITING:
        assign_manager(session, user)
    elif session.status == ChatSession.Status.BOT:
        session.status = ChatSession.Status.IN_PROGRESS
        session.assigned_to = user
        session.save(update_fields=['status', 'assigned_to', 'updated_at'])
    return add_message(session, sender_type=ChatMessage.SenderType.MANAGER, text=text)
