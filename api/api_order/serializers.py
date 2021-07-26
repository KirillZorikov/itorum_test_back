import re

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from . import models

User = get_user_model()


class CustomerRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.user.username

    def to_internal_value(self, data):
        try:
            customer = models.Customer.objects.get(user__username=data)
        except (ValueError, models.Customer.DoesNotExist):
            raise ValidationError()
        return customer


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerRelatedField(queryset=models.Customer.objects.all())

    class Meta:
        model = models.Order
        fields = ('id', 'customer', 'price', 'created_at')


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username',
                                        queryset=models.Customer.objects.all())

    class Meta:
        model = models.Customer
        fields = ('id', 'user')


class WeekNumberSerializer(serializers.Serializer):
    week_number = serializers.CharField(required=False)

    def validate_week_number(self, value):
        """ check date format """
        if re.match(r'^\d{4}-W\d{1,2}$', value):
            return value
        raise ValidationError({
            'week_number': 'Неверный формат даты. Ожидается: %Y-W%W'
        })


class DeleteOrdersSerializer(serializers.Serializer):
    list_ids = serializers.ListField()

    def validate_list_ids(self, value):
        """ check if all the ids exist """
        count_obj = models.Order.objects.filter(id__in=value).count()
        if count_obj != len(value):
            raise ValidationError('Получены невалидные значения поля id.')
        return value
