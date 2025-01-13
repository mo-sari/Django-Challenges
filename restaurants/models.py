from django.db import models
from django.db.models.functions import Length
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from rest_framework.exceptions import ValidationError

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .manager import RestaurantManager
import logging

logger = logging.getLogger('add_rating')


class Restaurant(models.Model):
    class TypeChoices(models.TextChoices):
        INDIAN = 'IN', 'Indian'
        CHINESE = 'CH', 'Chinese'
        ITALIAN = 'IT', 'Italian'
        GREEK = 'GR', 'Greek'
        MEXICAN = 'MX', 'Mexican'
        FASTFOOD = 'FF', 'Fast Food'
        OTHER = 'OT', 'Other'

    name = models.CharField(max_length=100, )
    website = models.URLField(default='')
    date_opened = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    restaurant_type = models.CharField(max_length=2,
                                       choices=TypeChoices.choices)

    # newManager = RestaurantManager()

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name='ratings')
    rating = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'restaurant'],
                name='unique_user_restaurant_rating'
            )
        ]

    def __str__(self):
        return f"Rating: {self.rating}"

    def clean(self):
        rating = Rating.objects.filter(
            user=self.user, restaurant=self.restaurant).first()

        if rating:
            raise ValidationError(
                detail='This user has already rated this restaurant')

        return super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    @property
    def resturant_name_length(self):
        return len(self.restaurant.name)

    def restaurant_rating_count(self):
        return len(self.restaurant.ratings.all())


class Sale(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.SET_NULL, null=True, related_name='sales')
    income = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField()

    def __str__(self):
        return f'{self.restaurant.name} income: {self.income}'


class Staff(models.Model):
    name = models.CharField(max_length=100)
    restaurants = models.ManyToManyField(Restaurant, through='StaffRestaurant')


class StaffRestaurant(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    salary = models.PositiveIntegerField()


@receiver(post_save, sender=Rating)
def log_rating_add(sender, instance, created, *args, **kwargs):
    if created:
        logger.info('A new Rating was added')


class Comment(models.Model):
    text = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
