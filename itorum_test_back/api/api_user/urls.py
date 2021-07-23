from rest_framework.authtoken import views
from django.urls import include, path

from .views import register

auth_urls = [
    path('register/', register, name='register'),
    path('login/', views.obtain_auth_token, name='login'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
]
