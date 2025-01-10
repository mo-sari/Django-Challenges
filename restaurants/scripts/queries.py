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
    # Write a custom QuerySet method to get restaurants with a specific average rating.
    # rests = Restaurant.objects.prefetch_related('ratings') \
    #     .annotate(
    #     avg_rating=Avg('ratings__rating')
    #    ).filter(avg_rating__gte=3.5)

    # ratings = Rating.objects.filter(restaurant=OuterRef('pk')) \
    #                         .values('restaurant') \
    #                         .annotate(
    #                             avg_rating=Avg('rating')) \
    #                         .values('avg_rating')

    # rests = Restaurant.objects.annotate(
    #     avg_rating=Subquery(ratings)
    # ).filter(avg_rating__gte=3.5)

    # for rest in rests:
    #     print(rest.name, rest.id, rest.avg_rating)

    # ==============================================================
    # Create a QuerySet to find the most popular restaurant type.
    # popular_type = Restaurant.objects.values('restaurant_type') \
    #                                  .annotate(
    #                                      avg_rating=Avg('ratings__rating')) \
    #                                  .order_by('-avg_rating')[:1]

    top_rating = Rating.objects.filter(restaurant=OuterRef('pk')) \
                               .values('restaurant__restaurant_type') \
                               .annotate(avg_rating=Avg('rating')) \
                               .order_by('-avg_rating')[:1]


    print(top_rating)
