from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.timezone import make_aware
from django.db.utils import IntegrityError
from faker import Faker

from ...models import Customer, ExportAccess, Order
from .factories import UserFactory, CustomerFactory, OrderFactory

User = get_user_model()

NUM_CUSTOMERS = 15
NUM_ORDERS = 500
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'
EXPORT_ACCESS_USERNAME = 'test'
EXPORT_ACCESS_PASSWORD = 'test'


class Command(BaseCommand):
    help = 'Generate fake data'

    # @transaction.atomic
    def handle(self, *args, **kwargs):
        fake = Faker()
        models = [User, Customer, ExportAccess, Order]

        # delete old data
        for model in models:
            model.objects.all().delete()

        # create superuser
        User.objects.create_superuser(ADMIN_USERNAME,
                                      'fk@ya.ru',
                                      ADMIN_PASSWORD)

        # create user to access the export
        user = UserFactory()
        user.username = EXPORT_ACCESS_USERNAME
        user.set_password(EXPORT_ACCESS_PASSWORD)
        user.save()
        ExportAccess.objects.create(user=user)

        with transaction.atomic():
            # create customers
            for _ in range(NUM_CUSTOMERS):
                try:
                    CustomerFactory()
                except IntegrityError:
                    pass

            # create orders
            orders = []
            for _ in range(NUM_ORDERS):
                order = OrderFactory()
                orders.append(order)

            # update order's date
            for order in orders:
                order.created_at = make_aware(
                    fake.date_time_between(start_date='-30d')
                )
                order.save()
