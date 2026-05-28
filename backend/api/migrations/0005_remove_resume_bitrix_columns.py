"""Удаление ошибочно добавленных полей CRM из таблицы резюме."""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_quoteattachment'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE api_resume DROP COLUMN IF EXISTS bitrix_lead_id;'
                'ALTER TABLE api_resume DROP COLUMN IF EXISTS bitrix_synced_at;'
                'ALTER TABLE api_resume DROP COLUMN IF EXISTS bitrix_sync_error;'
                'ALTER TABLE api_resume DROP COLUMN IF EXISTS bitrix_stub_path;'
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
