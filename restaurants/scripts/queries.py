from rest_framework.exceptions import ValidationError
from restaurants.models import Restaurant, Rating, Sale, Staff, StaffRestaurant
from django.contrib.auth.models import User
from faker import Faker
from django.db import connection
from pprint import pprint
import random
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.db.models import Avg, CharField, Value, Sum
from django.db.models.functions import Coalesce, Greatest, Length, Concat


def run():
