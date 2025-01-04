from rest_framework.exceptions import ValidationError
from restaurants.models import Restaurant, Rating, Sale, Staff, StaffRestaurant
from django.contrib.auth.models import User
from faker import Faker
from django.db import connection
from pprint import pprint
import random
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.db.models import Avg, CharField, Value
from django.db.models.functions import Coalesce, Greatest, Length, Concat


def run():
    # rests = Restaurant.objects.values('name', len=Length('name'))
    # for i in rests:
    #     print(i)
    # ================================================================
    # rts = Rating.objects.values('user__username', 'restaurant__name')
    # for i in rts:
    #     print(i)
    # ================================================================
    # rts = Rating.objects.values_list('user__username', 'restaurant__name')
    # for i in rts:
    #     print(i)

    # pprint(connection.queries)
    # ================================================================

    # rests = Restaurant.objects.values_list('name', 'date_opened')
    # for i in rests:
    #     print(i)
    # ================================================================

    # rests = Restaurant.objects.values_list('name', flat=True)
    # print(rests)
    # ================================================================
    # rests = Restaurant.objects.annotate(name_chars=Length('name'))

    # for rest in rests:
    #     print(rest.name_chars)

    # rests = Restaurant.objects.annotate(s=Concat('name',
    #                                              Value(' [ Average Rating = '),
    #                                              Avg('ratings__rating',
    #                                                  default=0),
    #                                              Value(' ]'),
    #                                              output_field=CharField()))
    # ================================================================

    # s = Concat(
    #     'name',
    #     Value(' [ Average Rating = '),
    #     Avg('ratings__rating', default=0),
    #     Value(' ]'),
    #     output_field=CharField())

    # rests = Restaurant.objects.annotate(message=s).values('name', 'message')

    # for rest in rests:
    #     print(rest)
    # ================================================================

    # rests = Restaurant.objects.values('restaurant_type') \
    #                           .annotate(avg_ratings=Avg('ratings__rating'))

    # for i in rests:
    #     print(i)
    # pprint(connection.queries)
