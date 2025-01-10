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
    # Find restaurants with the longest name
    # length where the average rating is above 3.5

    rests_name_len = Restaurant.objects.annotate(
        avg_rating=Avg('ratings__rating'),
        name_len=Length('name')
    ).filter(avg_rating__gte=3.5).aggregate(max_name_len=Max('name_len'))['max_name_len']

    rests = Restaurant.objects.annotate(
        avg_rating=Avg('ratings__rating'),
        name_len=Length('name')
    ).filter(avg_rating__gte=3.5,
             name_len=rests_name_len)

    for rest in rests:
        print(rest)
