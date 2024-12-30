from restaurants.models import Restaurant, Rating, Sale
from django.contrib.auth.models import User
from faker import Faker
from django.db import connection
from pprint import pprint
import random
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.db.models import Avg, Count, Q, F, Value, Max, Min
from django.db.models.functions import Coalesce


def run():

    # Miller, Perry and Anderson 24
    # Green and Sons 15
    # Collins Ltd 9
    user = User.objects.get(id=19)
    restaurant = Restaurant.objects.get(id=15)

    # Rating.objects.create(
    #     user=user,
    #     restaurant=restaurant,
    #     rating=3
    # )

    rating = Rating(
        user=user,
        restaurant=restaurant,
        rating=3
    )
    rating.save()
