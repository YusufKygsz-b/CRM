from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path(_('admin/'), include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('crm_login/', admin.site.urls),
    path('', include('website.urls')),
]

urlpatterns += i18n_patterns(
    path('', include('website.urls')),  # Dil URL deseni için 'website' uygulamasını ekledim
)