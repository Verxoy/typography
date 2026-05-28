# Generated manually for CMS models

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_chat_staff_visible_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_id', models.SlugField(max_length=80, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_published', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Раздел каталога',
                'verbose_name_plural': 'Разделы каталога',
                'ordering': ['sort_order', 'title'],
            },
        ),
        migrations.CreateModel(
            name='ChatBotTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64, unique=True)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Шаблон чат-бота',
                'verbose_name_plural': 'Шаблоны чат-бота',
            },
        ),
        migrations.CreateModel(
            name='ChatEscalateKeyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=64, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Ключевое слово эскалации',
                'verbose_name_plural': 'Ключевые слова эскалации',
                'ordering': ['keyword'],
            },
        ),
        migrations.CreateModel(
            name='ChatFaqRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pattern', models.CharField(help_text='Регулярное выражение (Python re)', max_length=500)),
                ('reply', models.TextField()),
                ('priority', models.IntegerField(default=0, help_text='Больше — проверяется раньше')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Правило FAQ',
                'verbose_name_plural': 'Правила FAQ',
                'ordering': ['-priority', 'id'],
            },
        ),
        migrations.CreateModel(
            name='GraphicModuleSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_title', models.CharField(default='КАЛЕНДАРИ НА 2025 ГОД!', max_length=255)),
                ('banner_text', models.TextField(blank=True)),
                ('module_title', models.CharField(default='Графический модуль визуализации', max_length=255)),
                ('module_description', models.TextField(blank=True)),
                ('max_upload_mb', models.PositiveSmallIntegerField(default=10)),
                ('allowed_formats', models.CharField(default='jpg,jpeg,png,webp', help_text='Через запятую', max_length=120)),
                ('ink_limit_percent', models.PositiveSmallIntegerField(default=300)),
                ('black_generation', models.CharField(default='UCR', max_length=32)),
                ('color_profile', models.CharField(default='ISO Coated v2', max_length=64)),
                ('show_promo_banner', models.BooleanField(default=True)),
                ('disclaimer_text', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Настройки графического модуля',
                'verbose_name_plural': 'Настройки графического модуля',
            },
        ),
        migrations.CreateModel(
            name='QuoteServiceConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=list)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Каталог быстрого расчёта',
                'verbose_name_plural': 'Каталог быстрого расчёта',
            },
        ),
        migrations.CreateModel(
            name='CatalogProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, db_index=True, max_length=120)),
                ('image_url', models.CharField(blank=True, max_length=500)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_published', models.BooleanField(default=True)),
                (
                    'section',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='products',
                        to='api.catalogsection',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Позиция каталога',
                'verbose_name_plural': 'Позиции каталога',
                'ordering': ['sort_order', 'title'],
            },
        ),
        migrations.CreateModel(
            name='CatalogProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.JSONField(default=dict)),
                (
                    'product',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='detail',
                        to='api.catalogproduct',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Страница продукта',
                'verbose_name_plural': 'Страницы продуктов',
            },
        ),
        migrations.AddConstraint(
            model_name='catalogproduct',
            constraint=models.UniqueConstraint(
                condition=models.Q(('slug', ''), _negated=True),
                fields=('section', 'slug'),
                name='unique_product_slug_per_section',
            ),
        ),
    ]
