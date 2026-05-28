from django.contrib import admin

from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static



from api.views_spa import SpaAssetView, SpaStaffView



spa_asset = SpaAssetView()

spa_staff = SpaStaffView()



urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),

    # Собранный Vue (vue-project/dist) — CRM-ссылки /staff/… работают на порту Django

    path('assets/<path:path>', spa_asset),

    path('staff/', spa_staff),

    path('staff/<path:path>', spa_staff),

]



if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

