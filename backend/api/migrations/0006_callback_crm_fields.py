from django.db import migrations, models
from django.utils import timezone


def fill_callback_public_numbers(apps, schema_editor):
    Callback = apps.get_model('api', 'CallbackRequest')
    year = timezone.now().year
    prefix = f'CB-{year}-'
    for idx, cb in enumerate(Callback.objects.order_by('id'), start=1):
        if not cb.public_number:
            cb.public_number = f'{prefix}{idx:04d}'
        if not getattr(cb, 'site_status', None):
            cb.site_status = 'closed' if cb.is_called else 'new'
        cb.save(update_fields=['public_number', 'site_status'])


class Migration(migrations.Migration):
    """Добавляет поля CRM для заявок на звонок (идемпотентно для частично обновлённой БД)."""

    dependencies = [
        ('api', '0005_remove_resume_bitrix_columns'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                    ALTER TABLE api_callbackrequest
                        ADD COLUMN IF NOT EXISTS public_number VARCHAR(32);
                    ALTER TABLE api_callbackrequest
                        ADD COLUMN IF NOT EXISTS site_status VARCHAR(20) NOT NULL DEFAULT 'new';
                    ALTER TABLE api_callbackrequest
                        ADD COLUMN IF NOT EXISTS manager_note TEXT NOT NULL DEFAULT '';
                    ALTER TABLE api_callbackrequest
                        ADD COLUMN IF NOT EXISTS bitrix_lead_id BIGINT NULL;
                    ALTER TABLE api_callbackrequest
                        ADD COLUMN IF NOT EXISTS bitrix_synced_at TIMESTAMP WITH TIME ZONE NULL;
                    ALTER TABLE api_callbackrequest
                        ADD COLUMN IF NOT EXISTS bitrix_sync_error TEXT NOT NULL DEFAULT '';
                    ALTER TABLE api_callbackrequest
                        ADD COLUMN IF NOT EXISTS bitrix_stub_path VARCHAR(500) NOT NULL DEFAULT '';
                    """,
                    reverse_sql=migrations.RunSQL.noop,
                ),
                migrations.RunPython(fill_callback_public_numbers, migrations.RunPython.noop),
                migrations.RunSQL(
                    sql="""
                    UPDATE api_callbackrequest
                    SET public_number = 'CB-LEGACY-' || LPAD(id::text, 4, '0')
                    WHERE public_number IS NULL OR public_number = '';
                    ALTER TABLE api_callbackrequest
                        ALTER COLUMN public_number SET NOT NULL;
                    CREATE UNIQUE INDEX IF NOT EXISTS api_callbackrequest_public_number_uniq
                        ON api_callbackrequest (public_number);
                    CREATE INDEX IF NOT EXISTS api_callbackrequest_created_at_idx
                        ON api_callbackrequest (created_at);
                    """,
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='callbackrequest',
                    name='public_number',
                    field=models.CharField(max_length=32, unique=True, verbose_name='Номер заявки'),
                ),
                migrations.AddField(
                    model_name='callbackrequest',
                    name='site_status',
                    field=models.CharField(
                        choices=[
                            ('new', 'Новая'),
                            ('in_review', 'В работе'),
                            ('closed', 'Перезвонили'),
                        ],
                        default='new',
                        max_length=20,
                        verbose_name='Статус на сайте',
                    ),
                ),
                migrations.AddField(
                    model_name='callbackrequest',
                    name='manager_note',
                    field=models.TextField(blank=True, default='', verbose_name='Заметка менеджера'),
                ),
                migrations.AddField(
                    model_name='callbackrequest',
                    name='bitrix_lead_id',
                    field=models.PositiveBigIntegerField(
                        blank=True, null=True, verbose_name='ID лида в Битрикс'
                    ),
                ),
                migrations.AddField(
                    model_name='callbackrequest',
                    name='bitrix_synced_at',
                    field=models.DateTimeField(
                        blank=True, null=True, verbose_name='Отправлено в CRM'
                    ),
                ),
                migrations.AddField(
                    model_name='callbackrequest',
                    name='bitrix_sync_error',
                    field=models.TextField(blank=True, default='', verbose_name='Ошибка CRM'),
                ),
                migrations.AddField(
                    model_name='callbackrequest',
                    name='bitrix_stub_path',
                    field=models.CharField(
                        blank=True, default='', max_length=500, verbose_name='Файл-заглушка CRM'
                    ),
                ),
                migrations.AlterField(
                    model_name='callbackrequest',
                    name='phone',
                    field=models.CharField(max_length=32, verbose_name='Телефон'),
                ),
                migrations.AlterField(
                    model_name='callbackrequest',
                    name='created_at',
                    field=models.DateTimeField(auto_now_add=True, db_index=True),
                ),
            ],
        ),
    ]
