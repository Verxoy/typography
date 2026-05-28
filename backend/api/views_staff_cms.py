"""API панели управления контентом (staff / administrator)."""
import re

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .cms_upload import save_cms_upload
from .models_cms import (
    CatalogProduct,
    CatalogProductDetail,
    CatalogSection,
    ChatBotTemplate,
    ChatEscalateKeyword,
    ChatFaqRule,
    GraphicModuleSettings,
    PortfolioWork,
    QuoteServiceConfig,
)
from .permissions import IsSiteAdministrator, IsSiteStaff
from .roles import is_site_administrator
from .quote_catalog import QUOTE_SERVICES
from .serializers_cms import (
    CatalogProductDetailSerializer,
    CatalogProductSerializer,
    CatalogProductWriteSerializer,
    CatalogSectionSerializer,
    ChatBotTemplateSerializer,
    ChatEscalateKeywordSerializer,
    ChatFaqRuleSerializer,
    GraphicModuleSettingsSerializer,
    PortfolioWorkSerializer,
    QuoteServiceConfigSerializer,
    StaffUserSerializer,
)
from . import chat_bot_loader

User = get_user_model()


class StaffCatalogSectionListView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsSiteStaff()]
        return [IsSiteAdministrator()]

    def get(self, request):
        qs = CatalogSection.objects.all()
        return Response(CatalogSectionSerializer(qs, many=True).data)

    def post(self, request):
        ser = CatalogSectionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


class StaffCatalogSectionDetailView(APIView):
    permission_classes = [IsSiteAdministrator]

    def get_object(self, pk: int) -> CatalogSection:
        return CatalogSection.objects.get(pk=pk)

    def get(self, request, pk: int):
        return Response(CatalogSectionSerializer(self.get_object(pk)).data)

    def patch(self, request, pk: int):
        obj = self.get_object(pk)
        ser = CatalogSectionSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    def delete(self, request, pk: int):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffCatalogProductListView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsSiteStaff()]
        return [IsSiteAdministrator()]

    def get(self, request):
        qs = CatalogProduct.objects.select_related('section').all()
        section_id = request.query_params.get('section')
        if section_id:
            qs = qs.filter(section__section_id=section_id)
        return Response(CatalogProductSerializer(qs, many=True).data)

    def post(self, request):
        ser = CatalogProductWriteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        product = ser.save()
        return Response(
            CatalogProductSerializer(product).data,
            status=status.HTTP_201_CREATED,
        )


class StaffCatalogProductDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ('GET', 'PATCH'):
            return [IsSiteStaff()]
        return [IsSiteAdministrator()]

    def get_object(self, pk: int) -> CatalogProduct:
        return CatalogProduct.objects.select_related('section').get(pk=pk)

    def get(self, request, pk: int):
        return Response(CatalogProductSerializer(self.get_object(pk)).data)

    def patch(self, request, pk: int):
        obj = self.get_object(pk)
        if is_site_administrator(request.user):
            ser = CatalogProductWriteSerializer(obj, data=request.data, partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response(CatalogProductSerializer(obj).data)
        if 'image_url' not in request.data:
            return Response(
                {'detail': 'Можно изменить только image_url.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.image_url = str(request.data.get('image_url') or '')
        obj.save(update_fields=['image_url'])
        return Response(CatalogProductSerializer(obj).data)

    def delete(self, request, pk: int):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffCatalogProductPageView(APIView):
    permission_classes = [IsSiteAdministrator]

    def get(self, request, slug: str):
        product = CatalogProduct.objects.filter(slug=slug).first()
        if not product:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        detail, _ = CatalogProductDetail.objects.get_or_create(
            product=product,
            defaults={'content': {}},
        )
        return Response(CatalogProductDetailSerializer(detail).data)

    def put(self, request, slug: str):
        product = CatalogProduct.objects.filter(slug=slug).first()
        if not product:
            return Response({'detail': 'Не найдено.'}, status=status.HTTP_404_NOT_FOUND)
        content = request.data.get('content')
        if not isinstance(content, dict):
            return Response(
                {'detail': 'Поле content должно быть объектом.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        detail, _ = CatalogProductDetail.objects.get_or_create(product=product)
        detail.content = content
        detail.save(update_fields=['content'])
        return Response(CatalogProductDetailSerializer(detail).data)


class StaffGraphicSettingsView(APIView):
    permission_classes = [IsSiteAdministrator]

    def get(self, request):
        return Response(GraphicModuleSettingsSerializer(GraphicModuleSettings.get_solo()).data)

    def put(self, request):
        obj = GraphicModuleSettings.get_solo()
        ser = GraphicModuleSettingsSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class StaffChatFaqListView(APIView):
    permission_classes = [IsSiteStaff]

    def get(self, request):
        qs = ChatFaqRule.objects.all()
        return Response(ChatFaqRuleSerializer(qs, many=True).data)

    def post(self, request):
        ser = ChatFaqRuleSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        pattern = ser.validated_data['pattern']
        try:
            re.compile(pattern)
        except re.error as e:
            return Response({'pattern': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        rule = ser.save()
        chat_bot_loader.invalidate_cache()
        return Response(ChatFaqRuleSerializer(rule).data, status=status.HTTP_201_CREATED)


class StaffChatFaqDetailView(APIView):
    permission_classes = [IsSiteStaff]

    def patch(self, request, pk: int):
        rule = ChatFaqRule.objects.get(pk=pk)
        ser = ChatFaqRuleSerializer(rule, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        if 'pattern' in ser.validated_data:
            try:
                re.compile(ser.validated_data['pattern'])
            except re.error as e:
                return Response({'pattern': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ser.save()
        chat_bot_loader.invalidate_cache()
        return Response(ser.data)

    def delete(self, request, pk: int):
        ChatFaqRule.objects.filter(pk=pk).delete()
        chat_bot_loader.invalidate_cache()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffChatTemplatesView(APIView):
    permission_classes = [IsSiteStaff]

    def get(self, request):
        return Response(ChatBotTemplateSerializer(ChatBotTemplate.objects.all(), many=True).data)

    def put(self, request):
        items = request.data.get('templates')
        if not isinstance(items, list):
            return Response(
                {'detail': 'Ожидается templates: [{key, text}, ...]'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for item in items:
            key = (item.get('key') or '').strip()
            text = item.get('text') or ''
            if not key:
                continue
            ChatBotTemplate.objects.update_or_create(key=key, defaults={'text': text})
        chat_bot_loader.invalidate_cache()
        return Response(ChatBotTemplateSerializer(ChatBotTemplate.objects.all(), many=True).data)


class StaffChatKeywordsView(APIView):
    permission_classes = [IsSiteStaff]

    def get(self, request):
        return Response(ChatEscalateKeywordSerializer(ChatEscalateKeyword.objects.all(), many=True).data)

    def put(self, request):
        keywords = request.data.get('keywords')
        if not isinstance(keywords, list):
            return Response(
                {'detail': 'Ожидается keywords: [строка, ...]'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ChatEscalateKeyword.objects.all().delete()
        for kw in keywords:
            k = str(kw).strip().lower()
            if k:
                ChatEscalateKeyword.objects.create(keyword=k)
        chat_bot_loader.invalidate_cache()
        return Response(ChatEscalateKeywordSerializer(ChatEscalateKeyword.objects.all(), many=True).data)


class StaffQuoteCatalogView(APIView):
    permission_classes = [IsSiteAdministrator]

    def get(self, request):
        cfg = QuoteServiceConfig.get_solo()
        data = cfg.data if cfg.data else [s for s in QUOTE_SERVICES]
        return Response({'data': data, 'updated_at': cfg.updated_at})

    def put(self, request):
        data = request.data.get('data')
        if not isinstance(data, list):
            return Response(
                {'detail': 'Поле data должно быть массивом.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cfg = QuoteServiceConfig.get_solo()
        cfg.data = data
        cfg.save(update_fields=['data', 'updated_at'])
        return Response(QuoteServiceConfigSerializer(cfg).data)


class StaffPortfolioListView(APIView):
    permission_classes = [IsSiteStaff]

    def get(self, request):
        qs = PortfolioWork.objects.all()
        return Response(PortfolioWorkSerializer(qs, many=True).data)

    def post(self, request):
        ser = PortfolioWorkSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        work = ser.save()
        return Response(PortfolioWorkSerializer(work).data, status=status.HTTP_201_CREATED)


class StaffPortfolioDetailView(APIView):
    permission_classes = [IsSiteStaff]

    def get_object(self, pk: int) -> PortfolioWork:
        return PortfolioWork.objects.get(pk=pk)

    def patch(self, request, pk: int):
        obj = self.get_object(pk)
        ser = PortfolioWorkSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    def delete(self, request, pk: int):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffCmsMediaUploadView(APIView):
    permission_classes = [IsSiteStaff]

    def post(self, request):
        uploaded = request.FILES.get('file')
        if not uploaded:
            return Response(
                {'detail': 'Файл не передан (поле file).'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subdir = (request.data.get('folder') or 'cms').strip().lower()
        if subdir not in ('cms', 'portfolio', 'catalog'):
            subdir = 'cms'
        try:
            url = save_cms_upload(uploaded, subdir=subdir)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'url': url})


class StaffUserListView(APIView):
    permission_classes = [IsSiteAdministrator]

    def get(self, request):
        qs = User.objects.filter(
            Q(groups__name__in=['Администратор', 'Менеджер']) | Q(is_superuser=True)
        ).distinct()
        return Response(StaffUserSerializer(qs, many=True).data)

    def post(self, request):
        ser = StaffUserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response(StaffUserSerializer(user).data, status=status.HTTP_201_CREATED)


class StaffUserDetailView(APIView):
    permission_classes = [IsSiteAdministrator]

    def get(self, request, pk: int):
        user = User.objects.get(pk=pk)
        return Response(StaffUserSerializer(user).data)

    def patch(self, request, pk: int):
        user = User.objects.get(pk=pk)
        if user.pk == request.user.pk and request.data.get('is_active') is False:
            return Response(
                {'detail': 'Нельзя деактивировать свою учётную запись.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ser = StaffUserSerializer(user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(StaffUserSerializer(user).data)

    def delete(self, request, pk: int):
        user = User.objects.get(pk=pk)
        if user.pk == request.user.pk:
            return Response(
                {'detail': 'Нельзя удалить свою учётную запись.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)
