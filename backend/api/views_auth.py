from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .roles import is_site_administrator, is_site_manager, is_site_staff


@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def auth_csrf(request):
    return Response({'csrfToken': get_token(request)})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def auth_login(request):
    username = (request.data.get('username') or '').strip()
    password = request.data.get('password') or ''
    user = authenticate(request, username=username, password=password)
    if user is None or not user.is_active:
        return Response({'detail': 'Неверный логин или пароль.'}, status=status.HTTP_400_BAD_REQUEST)
    if not is_site_staff(user):
        return Response(
            {'detail': 'Доступ только для сотрудников типографии.'},
            status=status.HTTP_403_FORBIDDEN,
        )
    login(request, user)
    return Response(_user_payload(user))


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def auth_logout(request):
    logout(request)
    return Response({'ok': True})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def auth_me(request):
    if not is_site_staff(request.user):
        return Response({'detail': 'Нет доступа.'}, status=status.HTTP_403_FORBIDDEN)
    return Response(_user_payload(request.user))


def _user_payload(user):
    return {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'is_administrator': is_site_administrator(user),
        'is_manager': is_site_manager(user),
    }
