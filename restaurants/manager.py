from django.db import models


class RestaurantQuerySet(models.QuerySet):
    def get_restaurants_ratings(self, id):
        print('From QuerySet', self)
        return self.get(id=id).ratings.all()


class RestaurantManager(models.Manager):
    def get_queryset(self):
        return RestaurantQuerySet(self.model, using=self._db)

    def get_restaurants_ratings(self, id):
        print('From Manager', self)
        return self.get_queryset().get_restaurants_ratings(id)
