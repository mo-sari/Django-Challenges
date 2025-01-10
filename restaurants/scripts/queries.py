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
    # Implement a view to get all users who rated a specific restaurant.
    rest_id = 11
    rest_ratings = Rating.objects.filter(restaurant__id=rest_id).values('user')

    print(rest_ratings)
