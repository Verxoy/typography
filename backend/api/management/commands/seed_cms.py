"""Начальное наполнение CMS: каталог, чат-бот, графический модуль, быстрый расчёт."""
import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand

from api import chat_bot as chat_bot_defaults
from api.catalog_seed_data import HOME_SECTION_IMAGES, PRODUCT_IMAGES, SECTIONS
from api.models_cms import (
    CatalogProduct,
    CatalogProductDetail,
    CatalogSection,
    ChatBotTemplate,
    ChatEscalateKeyword,
    ChatFaqRule,
    GraphicModuleSettings,
    PortfolioWork,
    QuoteServiceConfig,
)
from api.quote_catalog import QUOTE_SERVICES


class Command(BaseCommand):
    help = 'Заполнить БД контентом каталога, чат-бота и настроек (идемпотентно).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--import-details',
            action='store_true',
            help='Импортировать JSON страниц продуктов из fixtures/catalog_details.json',
        )

    def handle(self, *args, **options):
        self._seed_catalog()
        self._seed_portfolio()
        self._seed_chat()
        self._seed_graphic()
        self._seed_quotes()
        if options['import_details']:
            self._import_product_details()
        self.stdout.write(self.style.SUCCESS('CMS: данные обновлены.'))

    def _seed_catalog(self) -> None:
        for si, sec_data in enumerate(SECTIONS):
            home_image = HOME_SECTION_IMAGES.get(sec_data['section_id'], '')
            section, created = CatalogSection.objects.update_or_create(
                section_id=sec_data['section_id'],
                defaults={
                    'title': sec_data['title'],
                    'sort_order': si,
                    'is_published': True,
                },
            )
            if created or not section.home_image_url:
                section.home_image_url = home_image
                section.save(update_fields=['home_image_url'])
            for pi, prod in enumerate(sec_data['products']):
                slug = prod.get('slug') or ''
                image_url = PRODUCT_IMAGES.get(slug, '') if slug else ''
                lookup = {'section': section, 'slug': slug} if slug else {'section': section, 'title': prod['title']}
                CatalogProduct.objects.update_or_create(
                    **lookup,
                    defaults={
                        'title': prod['title'],
                        'slug': slug,
                        'sort_order': pi,
                        'image_url': image_url,
                        'is_published': True,
                    },
                )

    def _seed_portfolio(self) -> None:
        if PortfolioWork.objects.exists():
            return
        samples = [
            ('Календарь настенный', '/images/home-kalendari.png', 'Печать календарей'),
            ('Визитки', '/images/home-reklamnaya-poligrafiya.png', 'Визитки и полиграфия'),
            ('Упаковка', '/images/home-upakovka.png', 'Упаковка для бренда'),
            ('Сувенирная продукция', '/images/home-suveniry.png', 'Сувениры'),
            ('Ресторанная полиграфия', '/images/home-horeca.png', 'Меню и POS-материалы'),
        ]
        for i, (title, url, alt) in enumerate(samples):
            PortfolioWork.objects.create(
                title=title,
                image_url=url,
                alt_text=alt,
                sort_order=i,
                is_published=True,
            )

    def _seed_chat(self) -> None:
        templates = {
            'welcome': chat_bot_defaults.WELCOME_TEXT,
            'default_reply': chat_bot_defaults.DEFAULT_REPLY,
            'escalate_prompt': chat_bot_defaults.ESCALATE_PROMPT,
            'escalate_confirm': chat_bot_defaults.ESCALATE_CONFIRM,
            'contact_thanks': chat_bot_defaults.CONTACT_THANKS,
            'manager_joined': chat_bot_defaults.MANAGER_JOINED,
        }
        for key, text in templates.items():
            ChatBotTemplate.objects.update_or_create(key=key, defaults={'text': text})

        if not ChatEscalateKeyword.objects.exists():
            for kw in chat_bot_defaults.ESCALATE_KEYWORDS:
                ChatEscalateKeyword.objects.get_or_create(keyword=kw)

        if not ChatFaqRule.objects.exists():
            for i, (pattern, reply) in enumerate(chat_bot_defaults.FAQ):
                ChatFaqRule.objects.create(
                    pattern=pattern.pattern,
                    reply=reply,
                    priority=len(chat_bot_defaults.FAQ) - i,
                    is_active=True,
                )

    def _seed_graphic(self) -> None:
        GraphicModuleSettings.get_solo()
        obj = GraphicModuleSettings.objects.get(pk=1)
        if obj.module_title in (
            '',
            'Модуль визуализации продукции',
            'Модуль визуализации',
        ):
            obj.module_title = 'Графический модуль визуализации'
            obj.save(update_fields=['module_title'])
        new_desc = 'Выберите цвет для просмотра в цветовой модели CMYK'
        if not obj.module_description or 'Загрузите изображение для просмотра' in obj.module_description:
            obj.module_description = new_desc
            obj.banner_text = (
                'Мы создаем и производим любые типы календарей, а если потребуется, '
                'разработаем для Вас уникальный макет с учетом всех Ваших пожеланий.'
            )
            obj.save()

    def _seed_quotes(self) -> None:
        cfg = QuoteServiceConfig.get_solo()
        if not cfg.data:
            cfg.data = [dict(s) for s in QUOTE_SERVICES]
            cfg.save(update_fields=['data'])

    def _import_product_details(self) -> None:
        path = Path(__file__).resolve().parents[2] / 'fixtures' / 'catalog_details.json'
        if not path.is_file():
            self.stdout.write(self.style.WARNING(f'Нет файла {path}'))
            return
        pages = json.loads(path.read_text(encoding='utf-8'))
        for slug, content in pages.items():
            product = CatalogProduct.objects.filter(slug=slug).first()
            if not product:
                continue
            CatalogProductDetail.objects.update_or_create(
                product=product,
                defaults={'content': content},
            )
        self.stdout.write(self.style.SUCCESS(f'Импортировано страниц: {len(pages)}'))
