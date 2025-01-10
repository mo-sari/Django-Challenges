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
    # the sql query we're about to write in django orm
    # SELECT * FROM restaurants_sale
    # WHERE restaurant_id IN
    #     (SELECT id from restaurants_restaurant WHERE restaurant_type IN ('IT', 'CH'))

    # without Subquery:
    #     Sale.objects.filter(restaurant__restaurant_type__in=['IT', 'CH'])

    # with subquery
    # rests = Restaurant.objects.filter(restaurant_type__in=['IT', 'CH'])
    # sales = Sale.objects.filter(restaurant__in=Subquery(rests.values('pk')))

    # print(len(sales))
    # for sale in sales:
    #     print(sale)

    # ==========================================================================
    # annotate each Restaurant with the income generated from its MOST RECENT sale

    # restaurants = Restaurant.objects.all()

    # sale = Sale.objects.filter(restaurant=OuterRef('pk')) \
    #                    .order_by('-datetime')[:1]
    # restaurants = restaurants.annotate(
    #     latest_sale=Subquery(sale.values('income'))
    # )

    # for restaurant in restaurants:
    #     print(restaurant.name, restaurant.latest_sale)
    # ==========================================================================
    # filter to restaurants that have any sales with income > 85

    # sales = Sale.objects.filter(restaurant=OuterRef('pk'), income__gt=2500)
    # restaurants = Restaurant.objects.filter(
    #     Exists(sales)
    # )

    # for rest in restaurants:
    #     print(rest.name)
    # ==========================================================================
    # filter restaurants that have at least one five star rating
    # ratings = Rating.objects.filter(restaurant=OuterRef('pk'), rating__gte=5)
    # rests = Restaurant.objects.filter(
    #     Exists(ratings)
    # )
    # for rest in rests:
    #     print(rest.name)
    # ==========================================================================
    # just the inversion of previous query
    # ratings = Rating.objects.filter(restaurant=OuterRef('pk'), rating__gte=5)
    # rests = Restaurant.objects.filter(
    #     ~Exists(ratings)
    # )
    # for rest in rests:
    #     print(rest.name)
    # ==========================================================================
    # restaurants that had sales in the last five days
    last_five_days = timezone.now() - timedelta(days=1000)
    sales = Sale.objects.filter(restaurant=OuterRef('pk'),
                                datetime__gt=last_five_days)
    rests = Restaurant.objects.filter(
        Exists(sales)
    )
    for rest in rests:
        print(rest.name)
