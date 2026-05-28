"""Контент сайта: каталог, чат-бот, графический модуль."""
from django.db import models


class CatalogSection(models.Model):
    section_id = models.SlugField(max_length=80, unique=True)
    title = models.CharField(max_length=255)
    home_image_url = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='Фото карточки на главной',
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'title']
        verbose_name = 'Раздел каталога'
        verbose_name_plural = 'Разделы каталога'

    def __str__(self) -> str:
        return self.title


class CatalogProduct(models.Model):
    section = models.ForeignKey(
        CatalogSection,
        on_delete=models.CASCADE,
        related_name='products',
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=120, blank=True, db_index=True)
    image_url = models.CharField(max_length=500, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'title']
        verbose_name = 'Позиция каталога'
        verbose_name_plural = 'Позиции каталога'
        constraints = [
            models.UniqueConstraint(
                fields=['section', 'slug'],
                condition=~models.Q(slug=''),
                name='unique_product_slug_per_section',
            ),
        ]

    def __str__(self) -> str:
        return self.title


class CatalogProductDetail(models.Model):
    product = models.OneToOneField(
        CatalogProduct,
        on_delete=models.CASCADE,
        related_name='detail',
    )
    content = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Страница продукта'
        verbose_name_plural = 'Страницы продуктов'

    def __str__(self) -> str:
        return f'Детали: {self.product.title}'


class GraphicModuleSettings(models.Model):
    """Одна запись — настройки графического модуля."""

    banner_title = models.CharField(max_length=255, default='КАЛЕНДАРИ НА 2025 ГОД!')
    banner_text = models.TextField(blank=True)
    module_title = models.CharField(
        max_length=255,
        default='Графический модуль визуализации',
    )
    module_description = models.TextField(blank=True)
    max_upload_mb = models.PositiveSmallIntegerField(default=10)
    allowed_formats = models.CharField(
        max_length=120,
        default='jpg,jpeg,png,webp',
        help_text='Через запятую',
    )
    ink_limit_percent = models.PositiveSmallIntegerField(default=300)
    black_generation = models.CharField(max_length=32, default='UCR')
    color_profile = models.CharField(max_length=64, default='ISO Coated v2')
    show_promo_banner = models.BooleanField(default=True)
    disclaimer_text = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Настройки графического модуля'
        verbose_name_plural = 'Настройки графического модуля'

    def __str__(self) -> str:
        return 'Графический модуль'

    @classmethod
    def get_solo(cls) -> 'GraphicModuleSettings':
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ChatBotTemplate(models.Model):
    """Системные тексты чат-бота (ключ → текст)."""

    key = models.CharField(max_length=64, unique=True)
    text = models.TextField()

    class Meta:
        verbose_name = 'Шаблон чат-бота'
        verbose_name_plural = 'Шаблоны чат-бота'

    def __str__(self) -> str:
        return self.key


class ChatEscalateKeyword(models.Model):
    keyword = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['keyword']
        verbose_name = 'Ключевое слово эскалации'
        verbose_name_plural = 'Ключевые слова эскалации'

    def __str__(self) -> str:
        return self.keyword


class ChatFaqRule(models.Model):
    pattern = models.CharField(max_length=500, help_text='Регулярное выражение (Python re)')
    reply = models.TextField()
    priority = models.IntegerField(default=0, help_text='Больше — проверяется раньше')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-priority', 'id']
        verbose_name = 'Правило FAQ'
        verbose_name_plural = 'Правила FAQ'

    def __str__(self) -> str:
        return self.pattern[:60]


class PortfolioWork(models.Model):
    """Фото готовых работ на главной странице."""

    title = models.CharField(max_length=255, blank=True, default='', verbose_name='Подпись')
    image_url = models.CharField(max_length=500, verbose_name='Путь к изображению')
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Альтернативный текст',
    )
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Готовая работа'
        verbose_name_plural = 'Готовые работы'

    def __str__(self) -> str:
        return self.title or f'Работа #{self.pk}'


class QuoteServiceConfig(models.Model):
    """Услуги «Быстрый расчёт» — JSON как в quote_catalog.QUOTE_SERVICES."""

    data = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Каталог быстрого расчёта'
        verbose_name_plural = 'Каталог быстрого расчёта'

    def __str__(self) -> str:
        return 'Услуги быстрого расчёта'

    @classmethod
    def get_solo(cls) -> 'QuoteServiceConfig':
        obj, _ = cls.objects.get_or_create(pk=1, defaults={'data': []})
        return obj
