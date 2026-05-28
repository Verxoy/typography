"""Справочник услуг для «Быстрого расчёта»."""

_DEADLINE_OPTIONS = ['Не срочно', 'В течение 1–2 недель', 'Срочно', 'Пока не знаю']


def _order_fields(*, placeholder: str) -> list[dict]:
    return [
        {
            'key': 'opisanie',
            'label': 'Что нужно сделать',
            'type': 'textarea',
            'placeholder': placeholder,
            'required': True,
        },
        {
            'key': 'tirazh',
            'label': 'Тираж или количество (если знаете)',
            'type': 'text',
            'placeholder': 'Можно примерно: 200, 500, 1000…',
            'required': False,
        },
        {
            'key': 'srok',
            'label': 'Когда нужно',
            'type': 'select',
            'required': False,
            'options': _DEADLINE_OPTIONS,
        },
    ]


QUOTE_SERVICES = [
    {
        'slug': 'diskontnye-karty',
        'title': 'Дисконтные карты',
        'hint': 'Опишите задачу — формат, тираж и отделку можно указать примерно, остальное уточним при расчёте.',
        'fields': _order_fields(
            placeholder='Например: пластиковые карты, 500 шт., с вашим дизайном…',
        ),
    },
    {
        'slug': 'plakaty-postery',
        'title': 'Плакаты, постеры, афиши',
        'hint': 'Достаточно описать задачу — формат, тираж и срок подберём вместе, если не уверены.',
        'fields': _order_fields(
            placeholder='Например: постер А2, 200 шт., для мероприятия…',
        ),
    },
    {
        'slug': 'booklets',
        'title': 'Буклеты и каталоги',
        'hint': 'Укажите объём (страницы), формат и тираж, если знаете — остальное обсудим при расчёте.',
        'fields': _order_fields(
            placeholder='Например: каталог 32 страницы, тираж 200, на пружине…',
        ),
    },
    {
        'slug': 'horeca',
        'title': 'Меню для ресторанов и кафе',
        'hint': 'Опишите вид меню и тираж — формат и переплёт подскажем, если нужно.',
        'fields': _order_fields(
            placeholder='Например: меню на пружине, 30 позиций, 40 экземпляров…',
        ),
    },
    {
        'slug': 'kalendari',
        'title': 'Календари',
        'hint': 'Можно указать вид календаря, тираж и срок — параметры уточним вместе при расчёте.',
        'fields': _order_fields(
            placeholder='Например: настенный календарь, 12 листов, тираж 300…',
        ),
    },
    {
        'slug': 'wide-format',
        'title': 'Широкоформатная печать',
        'hint': 'Опишите размеры и количество — материал и сроки уточним при расчёте.',
        'fields': _order_fields(
            placeholder='Например: баннер 2×1 м, 3 шт., для улицы…',
        ),
    },
    {
        'slug': 'other',
        'title': 'Другое / не уверен в выборе',
        'hint': 'Опишите задачу своими словами — тираж, формат и срок можно указать примерно.',
        'fields': _order_fields(
            placeholder='Что печатаем, для чего, примерный тираж, сроки…',
        ),
    },
]

# Старые коды услуг — только для отображения заявок
LEGACY_QUOTE_SERVICES: dict[str, dict] = {
    'business-cards': {
        'slug': 'business-cards',
        'title': 'Визитки',
        'hint': '',
        'fields': [],
    },
    'leaflets': {
        'slug': 'leaflets',
        'title': 'Листовки и флаеры',
        'hint': '',
        'fields': [],
    },
    'reklamnaya-poligrafiya': {
        'slug': 'reklamnaya-poligrafiya',
        'title': 'Рекламная полиграфия',
        'hint': '',
        'fields': [],
    },
    'reklama-mps': {
        'slug': 'reklama-mps',
        'title': 'Реклама на местах продаж',
        'hint': '',
        'fields': [],
    },
    'upakovka': {
        'slug': 'upakovka',
        'title': 'Упаковка и этикетки',
        'hint': '',
        'fields': [],
    },
    'prepress': {
        'slug': 'prepress',
        'title': 'Дизайн и предпечатная подготовка',
        'hint': '',
        'fields': [],
    },
}


# Старые заявки могли сохраниться с английскими ключами
LEGACY_QUOTE_PARAM_LABELS = {
    'task': 'Что нужно сделать',
    'quantity': 'Тираж (если знаете)',
    'deadline': 'Когда нужно',
    'opisanie': 'Что нужно сделать',
    'tirazh': 'Тираж (если знаете)',
    'srok': 'Когда нужно',
}


def quote_param_label(key: str, service_slug: str | None = None) -> str:
    if service_slug:
        service = get_service(service_slug)
        if service:
            for field in service['fields']:
                if field['key'] == key:
                    return field['label']
    return LEGACY_QUOTE_PARAM_LABELS.get(key, key)


def get_parameter_rows(quote) -> list[dict[str, str]]:
    """Параметры заявки с русскими подписями для staff и CRM."""
    rows = []
    for key, value in (quote.parameters or {}).items():
        if value is None or str(value).strip() == '':
            continue
        rows.append({
            'key': key,
            'label': quote_param_label(key, quote.service_slug),
            'value': str(value),
        })
    return rows


def active_quote_services() -> list[dict]:
    try:
        from .models_cms import QuoteServiceConfig

        cfg = QuoteServiceConfig.get_solo()
        if cfg.data:
            return cfg.data
    except Exception:
        pass
    return QUOTE_SERVICES


def get_service(slug: str) -> dict | None:
    for item in active_quote_services():
        if item['slug'] == slug:
            return item
    legacy = LEGACY_QUOTE_SERVICES.get(slug)
    if legacy:
        return legacy
    return None
