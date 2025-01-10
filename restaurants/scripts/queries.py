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
    #  Find the average rating of restaurants
    #  that have been rated more than 2 times.

    # without subqueries solution

    # rests = Restaurant.objects.prefetch_related('ratings') \
    #                   .annotate(rat_count=Count('ratings')) \
    #                   .filter(rat_count__gte=2) \
    #                   .annotate(rat_avg=Avg('ratings__rating'))

    # for rest in rests:
    #     print(rest.id, rest.rat_avg)

    # solution with subqueries

    # ratings = Rating.objects.filter(restaurant=OuterRef('pk')) \
    #                         .values('restaurant') \
    #                         .annotate(rat_count=Count('rating')) \
    #                         .filter(rat_count__gte=2) \
    #                         .values('restaurant')

    # rests = Restaurant.objects.filter(id__in=Subquery(ratings)) \
    #                           .annotate(avg_rating=Avg('ratings__rating'))

    # print(rests)
    # pprint(connection.queries)
