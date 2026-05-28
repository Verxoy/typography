from django.db import migrations, models
from django.db.models import Min


def backfill_staff_visible_at(apps, schema_editor):
    ChatSession = apps.get_model('api', 'ChatSession')
    ChatMessage = apps.get_model('api', 'ChatMessage')

    visitor_times = {
        row['session_id']: row['first_at']
        for row in ChatMessage.objects.filter(sender_type='visitor')
        .values('session_id')
        .annotate(first_at=Min('created_at'))
    }

    to_update = []
    for session in ChatSession.objects.filter(staff_visible_at__isnull=True):
        visible_at = visitor_times.get(session.pk)
        if not visible_at and session.contact_submitted:
            visible_at = session.escalated_at or session.updated_at or session.created_at
        if visible_at:
            session.staff_visible_at = visible_at
            to_update.append(session)

    if to_update:
        ChatSession.objects.bulk_update(to_update, ['staff_visible_at'], batch_size=200)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_chat_bitrix_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatsession',
            name='staff_visible_at',
            field=models.DateTimeField(
                blank=True,
                db_index=True,
                null=True,
                verbose_name='В кабинете менеджера с',
            ),
        ),
        migrations.RunPython(backfill_staff_visible_at, migrations.RunPython.noop),
    ]
