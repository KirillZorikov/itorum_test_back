from datetime import datetime, timedelta

from django.contrib.postgres.aggregates import StringAgg
from django.db.models import Sum
from django.utils.timezone import make_aware
from django.db.models.functions import TruncDate

from .models import Order


def get_orders_by_week(week_number=None):
    if not week_number:
        week_number = datetime.now().strftime("%Y-W%V")
    data_from = make_aware(datetime.strptime(week_number + '-1', "%Y-W%W-%w"))
    data_to = data_from + timedelta(7)
    return Order.objects.filter(
        created_at__lt=data_to, created_at__gte=data_from
    ).annotate(
        day=TruncDate('created_at'),
        customers=StringAgg('customer__user__username', '; ', distinct=True)
    ).values('day', 'customers').annotate(total=Sum('price')).order_by('day')
