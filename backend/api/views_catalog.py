"""Публичный API каталога."""
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models_cms import CatalogProduct, CatalogProductDetail, CatalogSection


def _product_public_dict(p: CatalogProduct) -> dict:
    return {
        'id': f'{p.section.section_id}--{p.slug}' if p.slug else f'{p.section.section_id}--{p.id}',
        'title': p.title,
        'sectionId': p.section.section_id,
        'sectionTitle': p.section.title,
        'sortOrder': p.sort_order,
        'slug': p.slug or None,
        'imageUrl': p.image_url or None,
    }


class PublicCatalogView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        sections = CatalogSection.objects.filter(is_published=True).prefetch_related('products')
        products = []
        section_list = []
        for sec in sections:
            section_list.append(
                {
                    'id': sec.section_id,
                    'title': sec.title,
                    'sortOrder': sec.sort_order,
                    'homeImageUrl': sec.home_image_url or None,
                }
            )
            for p in sec.products.filter(is_published=True):
                products.append(_product_public_dict(p))
        return Response({'sections': section_list, 'products': products})


class PublicCatalogProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug: str):
        product = (
            CatalogProduct.objects.filter(slug=slug, is_published=True)
            .select_related('section')
            .first()
        )
        if not product:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            detail = product.detail
        except CatalogProductDetail.DoesNotExist:
            return Response({'detail': 'Страница не найдена.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                'slug': product.slug,
                'title': product.title,
                'content': detail.content,
            }
        )
