from rest_framework.exceptions import ValidationError
from restaurants.models import Restaurant, Rating, Sale, Staff, StaffRestaurant
from django.contrib.auth.models import User
from faker import Faker
from django.db import connection
from pprint import pprint
import random
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.db.models import Avg, CharField, Value, Sum, Case, When, Count, F, FloatField, IntegerField, Q
from django.db.models.functions import Coalesce, Greatest, Length, Concat


def run():
    # rests = Restaurant.objects.prefetch_related('sales').annotate(
    #     sales_count=Count('sales')
    # ).annotate(
    #     is_top_seller=Case(
    #         When(sales_count__gt=1, then=True),
    #         default=False
    #     )
    # )

    # pprint(
    #     rests.values('sales_count', 'is_top_seller')
    # )
    # pprint(
    #     rests.filter(is_top_seller=True)
    # )
    # =====================================================================
    # rests = Restaurant.objects.annotate(
    #     avg_rating=Coalesce(Avg('ratings__rating'), Value(0),
    #                         output_field=FloatField()),
    #     num_rating=Coalesce(Count('ratings__pk'), Value(0),
    #                         output_field=IntegerField())) \
    #                           .annotate(
    #                               rating_bucket=Case(
    #                                   When(avg_rating__gt=3.5,
    #                                        then=Value('Highly rated')),
    #                                   When(avg_rating__range=(2.5, 3.5),
    #                                        then=Value('Normal rated')),
    #                                   When(avg_rating__lt=2.5,
    #                                        then=Value('Bad rating')),
    #                                   default=Value('No ratings'),
    #                                   output_field=CharField()
    #                               )
    #                           )
    # pprint(
    #     rests.filter(rating_bucket='Highly rated')
    # )
    # pprint(
    #     rests.filter(rating_bucket='Normal rated')
    # )

    rst_type = Restaurant.TypeChoices

    Asian = Q(restaurant_type=rst_type.INDIAN) | \
        Q(restaurant_type=rst_type.CHINESE)

    European = Q(restaurant_type=rst_type.GREEK) | \
        Q(restaurant_type=rst_type.ITALIAN)

    South_American = Q(restaurant_type=rst_type.MEXICAN)

    rests = Restaurant.objects.annotate(
        continent=Case(
            When(Asian, then=Value('Asian')),
            When(European, then=Value('European')),
            When(South_American, then=Value('South American')),
            default=Value('N/A')
        )
    )

    pprint(
        rests.filter(continent='Asian')
    )
