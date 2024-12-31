from restaurants.models import Restaurant, Rating, Sale
from django.contrib.auth.models import User
from faker import Faker
from django.db import connection
from pprint import pprint
import random
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.db.models import Avg, Count, Q, F, Value, Max, Min, Sum, Prefetch
from django.db.models.functions import Coalesce, Greatest


def run():
    # month_ago = timezone.now() - timedelta(days=30)
    # monthly_sales = Prefetch(
    #     'sales',
    #     queryset=Sale.objects.filter(datetime__gte=month_ago)
    #     )

    # restaurants = Restaurant \
    #     .objects \
    #     .prefetch_related('ratings', monthly_sales) \
    #     .filter(ratings__rating=5)

    # # pprint(restaurants)
    # for rst in restaurants:

    #     for rate in rst.ratings.all():
    #         print(rate)

    #     for sale in rst.sales.all():
    #         print(sale)
    rests = Restaurant.objects.all()[0:2]
    for rest in rests:
        sales = rest.sales.all()

        print(sales)

    pprint(connection.queries)
