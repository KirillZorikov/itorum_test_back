from django.urls import include, path

from .views import register, CustomAuthToken

auth_urls = [
    path('register', register, name='register'),
    path('login', CustomAuthToken.as_view(), name='login'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
]
