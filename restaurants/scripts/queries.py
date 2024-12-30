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
    # Create a view to retrieve restaurants that belong to a given users highest-rated restaurant.
    # user = User.objects.get(id=39)
    # users_ratings = Rating.objects.filter(user=user).order_by('-rating')[0]

    # pprint(users_ratings.restaurant)

    user = User.objects.get(id=user_id)
    user_top_rating = user.rating_set.order_by('-rating').first()
    return user_top_rating.restaurant
