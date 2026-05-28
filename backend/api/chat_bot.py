"""Простые автоответы и эскалация на менеджера."""
from __future__ import annotations

import re
from dataclasses import dataclass

ESCALATE_KEYWORDS = (
    'менеджер',
    'оператор',
    'человек',
    'живой',
    'перезвон',
    'позвон',
    'связ',
    'не помог',
    'не понял',
)

FAQ: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r'срок|когда|сколько\s+дела|время\s+изготов', re.I),
        'Сроки зависят от тиража и вида продукции. Точный срок менеджер уточнит после расчёта — '
        'можете оформить «Быстрый расчёт» на сайте или попросить связаться с вами.',
    ),
    (
        re.compile(r'цен|стоим|прайс|сколько\s+стоит|расчёт|расчет', re.I),
        'Стоимость рассчитывается индивидуально по параметрам заказа. '
        'Удобнее всего — форма «Быстрый расчёт» в меню сайта. '
        'Могу передать вопрос менеджеру — напишите «менеджер».',
    ),
    (
        re.compile(r'визитк', re.I),
        'Визитки печатаем — оформите «Быстрый расчёт» (пункт «Другое») или напишите «менеджер».',
    ),
    (
        re.compile(r'листовк|флаер', re.I),
        'Листовки — в «Быстром расчёте» (плакаты/постеры или «Другое»). Нужна помощь — напишите «менеджер».',
    ),
    (
        re.compile(r'плакат|постер|афиш', re.I),
        'Плакаты и постеры — пункт «Плакаты, постеры, афиши» в «Быстром расчёте» на сайте.',
    ),
    (
        re.compile(r'дисконт|карт[аы]\s+лояль', re.I),
        'Дисконтные карты — отдельный пункт в «Быстром расчёте» на сайте.',
    ),
    (
        re.compile(r'меню|ресторан|кафе|бар\b', re.I),
        'Меню для ресторанов — пункт «Меню для ресторанов и кафе» в «Быстром расчёте».',
    ),
    (
        re.compile(r'календар', re.I),
        'Календари — отдельный пункт в «Быстром расчёте». Укажите вид и тираж примерно.',
    ),
    (
        re.compile(r'доставк|самовывоз|забрать', re.I),
        'Доставку и самовывоз согласуем с менеджером после подтверждения заказа. Напишите «менеджер», если нужны детали.',
    ),
    (
        re.compile(r'оплат|счёт|счет|безнал', re.I),
        'Работаем с юрлицами и физлицами, возможна оплата по счёту. Уточнения — у менеджера (напишите «менеджер»).',
    ),
    (
        re.compile(r'макет|дизайн|верстк', re.I),
        'Помогаем с макетами и дизайном. Пришлите ТЗ или макет через «Быстрый расчёт» (можно приложить файлы) '
        'или попросите менеджера — напишите «менеджер».',
    ),
    (
        re.compile(r'адрес|где\s+наход|как\s+доехать|офис', re.I),
        'Адрес и контакты — на странице «Контакты» сайта. Могу передать вопрос менеджеру — напишите «менеджер».',
    ),
    (
        re.compile(r'привет|здравств|добрый', re.I),
        'Здравствуйте! Я помогу с общими вопросами. Спросите про сроки, цены, доставку или напишите «менеджер», '
        'чтобы связаться с сотрудником.',
    ),
]

DEFAULT_REPLY = (
    'Спасибо за сообщение! Я могу подсказать по срокам, ценам, доставке и услугам. '
    'Если нужен ответ по вашему заказу — напишите «менеджер», и я передам диалог специалисту.'
)

WELCOME_TEXT = (
    'Здравствуйте! Я виртуальный помощник типографии. '
    'Спросите про сроки, стоимость или услуги — или напишите «менеджер», чтобы связаться с сотрудником.'
)

ESCALATE_PROMPT = 'Передаю диалог менеджеру. Заполните короткую форму ниже — менеджер свяжется с вами.'

ESCALATE_CONFIRM = (
    'Заявка передана менеджеру. Заполните форму ниже — так мы быстрее свяжемся с вами. '
    'Ответ менеджера появится в этом окне.'
)

CONTACT_THANKS = (
    'Спасибо! Заявка принята — менеджер свяжется с вами и ответит в этом чате.'
)

MANAGER_JOINED = 'Менеджер подключился к чату.'

_TEMPLATE_DEFAULTS = {
    'welcome': WELCOME_TEXT,
    'default_reply': DEFAULT_REPLY,
    'escalate_prompt': ESCALATE_PROMPT,
    'escalate_confirm': ESCALATE_CONFIRM,
    'contact_thanks': CONTACT_THANKS,
    'manager_joined': MANAGER_JOINED,
}


def _default_template(key: str) -> str:
    return _TEMPLATE_DEFAULTS.get(key, '')


@dataclass
class BotTurnResult:
    reply: str | None
    should_escalate: bool
    extract_contact: bool = False


def wants_escalation(text: str) -> bool:
    from . import chat_bot_loader

    cfg = chat_bot_loader.get_bot_config()
    low = text.lower().strip()
    if low in ('менеджер', 'оператор', 'человек', 'помощь'):
        return True
    return any(kw in low for kw in cfg.escalate_keywords)


def parse_name_phone(text: str) -> tuple[str, str]:
    """Простой разбор «Имя, +7…» из одного сообщения."""
    phone_match = re.search(r'\+?\d[\d\s\-()]{8,}\d', text)
    phone = phone_match.group(0).strip() if phone_match else ''
    name_part = text
    if phone_match:
        name_part = text[: phone_match.start()] + text[phone_match.end() :]
    name = re.sub(r'[,;]+', ' ', name_part).strip()
    name = re.sub(r'\s+', ' ', name).strip(' ,.-')
    return name[:200], phone[:32]


def bot_reply(text: str, *, already_waiting: bool) -> BotTurnResult:
    from . import chat_bot_loader

    cfg = chat_bot_loader.get_bot_config()
    if already_waiting:
        return BotTurnResult(reply=None, should_escalate=False)

    if wants_escalation(text):
        return BotTurnResult(reply=None, should_escalate=True)

    for pattern, answer in cfg.faq:
        if pattern.search(text):
            return BotTurnResult(reply=answer, should_escalate=False)

    return BotTurnResult(reply=cfg.templates.get('default_reply', DEFAULT_REPLY), should_escalate=False)


def get_template_text(key: str) -> str:
    from . import chat_bot_loader

    cfg = chat_bot_loader.get_bot_config()
    return cfg.templates.get(key, _default_template(key))
