from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_quoterequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quoterequest',
            name='company_name',
            field=models.CharField(
                blank=True, default='', max_length=300, verbose_name='Название организации'
            ),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='inn',
            field=models.CharField(
                blank=True, default='', db_index=True, max_length=12, verbose_name='ИНН'
            ),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='company_type',
            field=models.CharField(
                choices=[
                    ('ip', 'ИП'),
                    ('ooo', 'ООО'),
                    ('private', 'Частный заказ'),
                ],
                max_length=8,
                verbose_name='Тип юрлица',
            ),
        ),
    ]
