from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Customer(models.Model):
    """ Customer model. """
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='customers',
                                verbose_name='Заказчик',
                                help_text='Заказчик')

    class Meta:
        ordering = ('user__username',)
        get_latest_by = 'id'
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if Customer.objects.count() > 15:
            raise ValidationError('Попытка превышения максимального '
                                  'числа заказчиков. max=15')
        super().save(*args, **kwargs)


class ExportAccess(models.Model):
    """ Model of users who are allowed access to export orders. """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='allowed_to_export',
                             verbose_name='Пользователь',
                             help_text=('Пользователь с доступом к '
                                        'экспорту заказов'))

    class Meta:
        ordering = ('user__username',)
        get_latest_by = 'id'
        verbose_name = 'Доступ к экспорту'
        verbose_name_plural = 'Доступ к экспорту'

    def __str__(self):
        return self.user.username


class Order(models.Model):
    """ Order model. """
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 related_name='orders',
                                 verbose_name='Заказчик',
                                 help_text='Заказчик')
    price = models.IntegerField(db_index=True,
                                verbose_name='Сумма',
                                help_text='Сумма заказа')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата',
                                      help_text='Дата создания заказа')

    class Meta:
        ordering = ('-id',)
        get_latest_by = 'id'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.customer.user.username
