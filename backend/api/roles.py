GROUP_ADMINISTRATOR = 'Администратор'
GROUP_MANAGER = 'Менеджер'


def user_in_group(user, group_name: str) -> bool:
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()


def is_site_administrator(user) -> bool:
    if not user.is_authenticated or not user.is_active:
        return False
    if user.is_superuser:
        return True
    return user_in_group(user, GROUP_ADMINISTRATOR)


def is_site_manager(user) -> bool:
    if not user.is_authenticated or not user.is_active:
        return False
    return user_in_group(user, GROUP_MANAGER)


def is_site_staff(user) -> bool:
    return is_site_administrator(user) or is_site_manager(user)
