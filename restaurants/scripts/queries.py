from restaurants.models import Restaurant, Rating, Sale
from django.contrib.auth.models import User
from faker import Faker
from django.db import connection
from pprint import pprint
import random
from django.utils import timezone
from datetime import datetime, timedelta


def run():
    rest = Restaurant.objects.get(id=1)
    print(rest.date_opened.year)
    print((timezone.now() - timedelta(days=365)).year)
