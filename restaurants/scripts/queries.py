from restaurants.models import Restaurant, Rating, Sale
from django.contrib.auth.models import User
from faker import Faker
from django.db import connection
from pprint import pprint
import random
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.db.models import Avg, Count, Q, F, Value
from django.db.models.functions import Coalesce


def run():
    rests = Restaurant.objects.filter(
        Q(sales__income__gt=5_000) & Q(
            sales__datetime__date=date.fromisoformat('2024-09-15')))

    for i in rests:
        print(i)
