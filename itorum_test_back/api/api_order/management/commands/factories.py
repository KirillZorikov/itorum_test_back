import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

from ...models import Customer, Order

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('first_name')
    password = '1234'


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    user = factory.SubFactory(UserFactory)

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.Iterator(Customer.objects.all())
    price = factory.Faker('pyint', min_value=10)
