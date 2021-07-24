import re

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
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
    class Meta:
        model = models.Customer
        fields = ('id', 'user')


class ExportAccessSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'],
                            password=attrs['password'])
        if not user or not models.ExportAccess.objects.filter(user=user
                                                              ).exists():
            raise ValidationError({'credentials': 'Введены неверные данные.'})
        return attrs


class WeekNumberSerializer(serializers.Serializer):
    week_number = serializers.CharField()

    def validate_week_number(self, value):
        if re.match(r'^\d{4}-W\d{1,2}$', value):
            return value
        raise ValidationError({
            'week_number': 'Неверный формат даты. Ожидается: "%Y-W%W"'
        })
