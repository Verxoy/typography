# Generated manually for initial api models

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Обработано')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('age', models.IntegerField(verbose_name='Возраст')),
                ('education', models.CharField(max_length=300, verbose_name='Образование')),
                ('position', models.CharField(max_length=200, verbose_name='Желаемая должность')),
                ('salary', models.CharField(max_length=50, verbose_name='Желаемая зарплата')),
                ('experience', models.CharField(max_length=100, verbose_name='Опыт работы')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон WhatsApp')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('is_reviewed', models.BooleanField(default=False, verbose_name='Просмотрено')),
            ],
            options={
                'verbose_name': 'Резюме',
                'verbose_name_plural': 'Резюме',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CallbackRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_called', models.BooleanField(default=False, verbose_name='Перезвонили')),
            ],
            options={
                'verbose_name': 'Заявка на звонок',
                'verbose_name_plural': 'Заявки на звонок',
                'ordering': ['-created_at'],
            },
        ),
    ]
