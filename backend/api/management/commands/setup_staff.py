from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from api.roles import GROUP_ADMINISTRATOR, GROUP_MANAGER


class Command(BaseCommand):
    help = 'Создаёт группы «Администратор» и «Менеджер»; опционально — демо-менеджера для теста.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--demo-admin',
            action='store_true',
            help='Создать администратора admin / admin123 (группа Администратор, is_staff, is_superuser)',
        )
        parser.add_argument(
            '--demo-manager',
            action='store_true',
            help='Создать пользователя manager / manager123 в группе Менеджер',
        )

    def handle(self, *args, **options):
        for name in (GROUP_ADMINISTRATOR, GROUP_MANAGER):
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Группа создана: {name}'))
            else:
                self.stdout.write(f'Группа уже есть: {name}')

        if options['demo_admin']:
            user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'first_name': 'Администратор',
                    'is_staff': True,
                    'is_superuser': True,
                },
            )
            user.set_password('admin123')
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            group = Group.objects.get(name=GROUP_ADMINISTRATOR)
            user.groups.clear()
            user.groups.add(group)
            action = 'создан' if created else 'обновлён'
            self.stdout.write(
                self.style.SUCCESS(
                    f'Демо-администратор {action}: логин admin, пароль admin123\n'
                    f'  Кабинет: /staff/login\n'
                    f'  Django admin: /admin/'
                )
            )

        if options['demo_manager']:
            user, created = User.objects.get_or_create(
                username='manager',
                defaults={'first_name': 'Демо', 'last_name': 'Менеджер', 'is_staff': True},
            )
            user.set_password('manager123')
            user.is_active = True
            user.save()
            group = Group.objects.get(name=GROUP_MANAGER)
            user.groups.add(group)
            action = 'создан' if created else 'обновлён'
            self.stdout.write(
                self.style.SUCCESS(
                    f'Демо-менеджер {action}: логин manager, пароль manager123'
                )
            )
