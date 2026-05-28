"""Загрузка правил чат-бота из БД с кэшем и fallback на код."""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache

from . import chat_bot as chat_bot_defaults
from .models_cms import ChatBotTemplate, ChatEscalateKeyword, ChatFaqRule

TEMPLATE_KEYS = (
    'welcome',
    'default_reply',
    'escalate_prompt',
    'escalate_confirm',
    'contact_thanks',
    'manager_joined',
)


@dataclass
class BotConfig:
    faq: list[tuple[re.Pattern[str], str]]
    escalate_keywords: tuple[str, ...]
    templates: dict[str, str]


def invalidate_cache() -> None:
    get_bot_config.cache_clear()


@lru_cache(maxsize=1)
def get_bot_config() -> BotConfig:
    faq_db = list(
        ChatFaqRule.objects.filter(is_active=True).order_by('-priority', 'id')
    )
    if faq_db:
        faq: list[tuple[re.Pattern[str], str]] = []
        for rule in faq_db:
            try:
                faq.append((re.compile(rule.pattern, re.I), rule.reply))
            except re.error:
                continue
    else:
        faq = list(chat_bot_defaults.FAQ)

    kw_db = list(
        ChatEscalateKeyword.objects.filter(is_active=True).values_list('keyword', flat=True)
    )
    escalate_keywords = tuple(kw_db) if kw_db else chat_bot_defaults.ESCALATE_KEYWORDS

    templates = {k: chat_bot_defaults._default_template(k) for k in TEMPLATE_KEYS}  # noqa: SLF001
    for row in ChatBotTemplate.objects.filter(key__in=TEMPLATE_KEYS):
        templates[row.key] = row.text

    return BotConfig(faq=faq, escalate_keywords=escalate_keywords, templates=templates)
