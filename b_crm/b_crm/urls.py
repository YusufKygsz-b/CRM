from django.contrib import admin
from django.urls import path, include
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]
