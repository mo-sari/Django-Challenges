from rest_framework.exceptions import ValidationError
from restaurants.models import Restaurant, Rating, Sale, Staff, StaffRestaurant
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
    salaries = [28000, 29000, 20000, 30000]

    staff = [staff
             for staff in Staff.objects.all()
             ]

    rests = Restaurant.objects.all()

    for rest in rests:
        for j in range(0, random.randint(3, 6)):
            rest.staff_set.add(random.choice(staff),
                               through_defaults={'salary':
                               random.choice(salaries)})

    # this below is not good for differentiating
    # the value of each staff's salary

    # for rest in rests:
    #     rnd = random.randint(0, 5)
    #     rest.staff_set.set(
    #         random.choices(staff, k=rnd),
    #         through_defaults={'salary': random.choice(salaries)}
    #     )

    # staff = Staff.objects.annotate(count=Count('restaurants'))
    #     count = 0
    #     for i in staff:
    #         count += i.count

    #     print(count)
