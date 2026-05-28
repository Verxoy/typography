from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_cms_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=255, verbose_name='Подпись')),
                ('image_url', models.CharField(max_length=500, verbose_name='Путь к изображению')),
                ('alt_text', models.CharField(blank=True, default='', max_length=255, verbose_name='Альтернативный текст')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Готовая работа',
                'verbose_name_plural': 'Готовые работы',
                'ordering': ['sort_order', 'id'],
            },
        ),
    ]
