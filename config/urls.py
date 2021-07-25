from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path(f'{settings.PROJECT_NAME}/admin/', admin.site.urls),
    path(f'{settings.PROJECT_NAME}/api/', include('api.api_order.urls')),
    path(f'{settings.PROJECT_NAME}/api/', include('api.api_user.urls')),
]
