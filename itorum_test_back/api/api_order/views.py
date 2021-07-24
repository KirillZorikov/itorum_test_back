from rest_framework import mixins, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from . import utils
from . import serializers


class CustomerViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    pagination_class = None
    serializer_class = serializers.CustomerSerializer
    queryset = models.Customer.objects.all()
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('get',)


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class_default = serializers.OrderSerializer
    serializer_classes = {
        'export': serializers.ExportAccessSerializer,
        'open_list': serializers.WeekNumberSerializer
    }
    queryset = models.Order.objects.all()
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('get', 'post', 'delete')

    @action(detail=False,
            methods=('post',),
            permission_classes=(permissions.AllowAny,))
    def export(self, request):
        access_serializer = self.get_serializer(data=request.data)
        access_serializer.is_valid(raise_exception=True)
        serializer = self.serializer_class_default(self.get_queryset(),
                                                   many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=('post',),
            permission_classes=(permissions.AllowAny,))
    def open_list(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        orders = utils.get_orders_by_week(
            serializer.validated_data.get('week_number')
        )
        return Response(orders, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return self.serializer_class_default
