from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_portfolio_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogsection',
            name='home_image_url',
            field=models.CharField(
                blank=True,
                default='',
                max_length=500,
                verbose_name='Фото карточки на главной',
            ),
        ),
    ]
