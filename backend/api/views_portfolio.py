"""Публичный API блока «Готовые работы»."""
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models_cms import PortfolioWork


class PublicPortfolioView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = PortfolioWork.objects.filter(is_published=True).order_by('sort_order', 'id')
        items = [
            {
                'id': w.id,
                'title': w.title,
                'imageUrl': w.image_url,
                'altText': w.alt_text or w.title or 'Готовая работа',
            }
            for w in qs
        ]
        return Response({'items': items})
