from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_number', models.CharField(max_length=32, unique=True, verbose_name='Номер заявки')),
                ('service_slug', models.CharField(max_length=64, verbose_name='Код услуги')),
                ('service_title', models.CharField(max_length=200, verbose_name='Услуга')),
                ('parameters', models.JSONField(default=dict, verbose_name='Параметры заказа')),
                ('company_type', models.CharField(choices=[('ip', 'ИП'), ('ooo', 'ООО')], max_length=8, verbose_name='Тип юрлица')),
                ('company_name', models.CharField(max_length=300, verbose_name='Название организации')),
                ('inn', models.CharField(db_index=True, max_length=12, verbose_name='ИНН')),
                ('contact_name', models.CharField(max_length=200, verbose_name='Контактное лицо')),
                ('contact_phone', models.CharField(max_length=32, verbose_name='Телефон')),
                ('contact_email', models.EmailField(max_length=254, verbose_name='Email')),
                ('client_comment', models.TextField(blank=True, default='', verbose_name='Комментарий клиента')),
                (
                    'site_status',
                    models.CharField(
                        choices=[
                            ('new', 'Новая'),
                            ('in_review', 'В работе'),
                            ('kp_sent', 'КП отправлено'),
                            ('closed', 'Закрыта'),
                        ],
                        default='new',
                        max_length=20,
                        verbose_name='Статус на сайте',
                    ),
                ),
                ('manager_note', models.TextField(blank=True, default='', verbose_name='Заметка менеджера')),
                ('bitrix_lead_id', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='ID лида в Битрикс')),
                ('bitrix_synced_at', models.DateTimeField(blank=True, null=True, verbose_name='Отправлено в CRM')),
                ('bitrix_sync_error', models.TextField(blank=True, default='', verbose_name='Ошибка CRM')),
                ('bitrix_stub_path', models.CharField(blank=True, default='', max_length=500, verbose_name='Файл-заглушка CRM')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'verbose_name': 'Заявка на расчёт',
                'verbose_name_plural': 'Заявки на расчёт',
                'ordering': ['-created_at'],
            },
        ),
    ]
