from restaurants.models import Restaurant, Rating, Sale
from django.contrib.auth.models import User
from faker import Faker
from django.db import connection
from pprint import pprint
import random


def run():
    faker = Faker()

    users = []
    for _ in range(30):
        user = User.objects.create_user(
            username=faker.unique.user_name(),
            email=faker.unique.email(),
            password="password123"
        )
        users.append(user)

    # Populating Restaurants
    restaurants = []
    restaurant_types = Restaurant.TypeChoices.values
    for _ in range(30):
        restaurant = Restaurant.objects.create(
            name=faker.unique.company(),
            website=faker.url(),
            date_opened=faker.date_this_century(),
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180),
            restaurant_type=random.choice(restaurant_types)
        )
        restaurants.append(restaurant)

    # Populating Ratings
    for _ in range(30):
        Rating.objects.create(
            user=random.choice(users),
            restaurant=random.choice(restaurants),
            rating=random.randint(1, 5)
        )

    # Populating Sales
    for _ in range(30):
        Sale.objects.create(
            restaurant=random.choice(restaurants),
            income=round(random.uniform(500.00, 10000.00), 2),
            datetime=faker.date_time_this_year()
        )

    print("Database populated successfully!")
