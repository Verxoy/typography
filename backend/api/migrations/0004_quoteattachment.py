import api.models_quotes
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_quote_simpler_legal'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'file',
                    models.FileField(
                        upload_to=api.models_quotes.quote_attachment_upload_to,
                        verbose_name='Файл',
                    ),
                ),
                ('original_name', models.CharField(max_length=255, verbose_name='Имя файла')),
                ('content_type', models.CharField(blank=True, default='', max_length=120, verbose_name='MIME')),
                ('file_size', models.PositiveIntegerField(default=0, verbose_name='Размер (байт)')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                (
                    'quote',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='attachments',
                        to='api.quoterequest',
                        verbose_name='Заявка',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Вложение к заявке',
                'verbose_name_plural': 'Вложения к заявкам',
                'ordering': ['id'],
            },
        ),
    ]
