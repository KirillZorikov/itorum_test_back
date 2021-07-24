from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)

router.register(
    'customers',
    views.CustomerViewSet,
    basename='customers',
)
router.register(
    'orders',
    views.OrderViewSet,
    basename='orders',
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
