from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from rest_framework.routers import DefaultRouter
from website.views import SupplierViewSet

# Router'ı oluşturun ve API view'ını ekleyin
router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)

# URL desenlerini tanımlayın
urlpatterns = [
    path(_('admin/'), include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('crm_login/', admin.site.urls),
]

# Uluslararasılaştırma (i18n) desenlerini ekleyin
urlpatterns += i18n_patterns(
    path('', include('website.urls')),  # Diğer uygulama URL'lerini buraya ekleyin
    path('api/', include(router.urls)),  # API URL'lerini buraya ekleyin
)