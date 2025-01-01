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
    rest = Restaurant.newManager.get_restaurants_ratings(29)

    print(rest)
