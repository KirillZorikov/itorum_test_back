from rest_framework import mixins, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from . import utils
from . import serializers
from .permissions import IsAuthenticatedAndHasAccess


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
        'open_list': serializers.WeekNumberSerializer,
        'delete_list_orders': serializers.DeleteOrdersSerializer
    }
    queryset = models.Order.objects.all()
    http_method_names = ('get', 'post', 'delete')

    @action(detail=False,
            methods=('get',),
            permission_classes=(IsAuthenticatedAndHasAccess,))
    def export(self, request):
        serializer = self.get_serializer(self.get_queryset(),
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

    @action(detail=False,
            methods=('delete',))
    def delete_list_orders(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        list_ids = serializer.validated_data.get('list_ids')
        models.Order.objects.filter(id__in=list_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return self.serializer_class_default
