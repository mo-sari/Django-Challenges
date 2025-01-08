import random
from datetime import date, datetime, timedelta
from pprint import pprint

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import (Avg, Case, CharField, Count, F, FloatField,
                              IntegerField, Max, Q, Subquery, Sum, Value,
                              When, OuterRef, Exists)
from django.db.models.functions import Coalesce, Concat, Greatest, Length
from django.utils import timezone
from faker import Faker
from rest_framework.exceptions import ValidationError

from restaurants.models import Rating, Restaurant, Sale, Staff, StaffRestaurant


def run():
    # sales = Sale.objects.filter(restaurant__restaurant_type__in=['IT', "CH"])

    # pprint(
    #     len(sales)
    # )
    # we could write the exact same thing with Subquery

    # this below is the way to do it with subqueries

    # rests = Restaurant.objects.filter(restaurant_type__in=['IT', 'CH'])
    # sales = Sale.objects.filter(restaurant__in=Subquery(rests.values('pk')))

    # print(len(sales))
    # ==================================================================
    # annotate each restaurant with the income generated from its MOST RECENT sale

    # sales = Sale.objects.filter(restaurant=OuterRef('pk')) \
    #                     .order_by('-income') \

    # rests = Restaurant.objects.annotate(rest_last_sale=Subquery(
    #     sales.values('income')[:1]
    # ))

    # for rest in rests:
    #     print(rest.name, rest.rest_last_sale)
    # ==================================================================

    # filter to restaurants that have any sales with income > 2500
    # rests = Restaurant.objects.filter(
    #     Exists(Sale.objects.filter(
    #         restaurant=OuterRef('pk'),
    #         income__gt=2500
    #     ))
    # )

    # for rest in rests:
    #     print(rest.name)
    # ==================================================================

    # filter to restaurants that have a five star rating
    # rests = Restaurant.objects.filter(
    #     Exists(Rating.objects.filter(
    #         restaurant=OuterRef('pk'),
    #         rating=5
    #     ))
    # )

    # for rest in rests:
    #     print(rest.name)
    # ==================================================================

    # filter to restaurants that had a sale in the last five days
    rests = Restaurant.objects.filter(
        Exists(Sale.objects.filter(
            restaurant=OuterRef('pk'),
            datetime__gt=timezone.now() - timedelta(days=1000)
        ))
    )

    for rest in rests:
        print(rest.name)
