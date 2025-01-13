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
from django.contrib.contenttypes.models import ContentType


def run():
    content_type = ContentType.objects.get(
        app_label='restaurants',
        model='sale')
    print(content_type.model_class())

    print('====================================')

    sales = content_type.model_class()
    print(sales.objects.all())

    print('=================================')

    sale = content_type.get_object_for_this_type(
        restaurant__name='New name')
    print(sale)
