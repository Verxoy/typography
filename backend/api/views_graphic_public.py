"""Публичные настройки графического модуля."""
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models_cms import GraphicModuleSettings
from .serializers_cms import GraphicModuleSettingsSerializer


class PublicGraphicSettingsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(GraphicModuleSettingsSerializer(GraphicModuleSettings.get_solo()).data)
