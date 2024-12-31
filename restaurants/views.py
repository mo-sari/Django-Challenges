from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta, date

from restaurants import serializers
from restaurants.models import Restaurant, Sale
from restaurants.paginations import LimitedResultsSetPagination

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import (
    NotFound,
    ValidationError,
    PermissionDenied)
from django.db.models import Avg, Count, Value, Q
from django.db.models.functions import Coalesce
from django.db import connection
from pprint import pprint


class RestaurantsAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]
    # queryset = Restaurant.objects.all()
    pagination_class = LimitedResultsSetPagination

    def get_queryset(self):
        return Restaurant.objects.prefetch_related('ratings', 'sales')


class RestaurantAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        rst_name = self.kwargs['rst_name']
        try:
            return Restaurant.objects.get(name__iexact=rst_name)
        except Restaurant.DoesNotExist:
            raise NotFound(detail=f'Restaurant with name {rst_name} not found')


class RestaurantByTypeAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        rst_type = self.kwargs['rst_type']

        valid_types = [choice[0] for choice in Restaurant.TypeChoices.choices]
        if rst_type.upper() not in valid_types:
            raise ValidationError(
                detail=f'No Restaurant was found by the type of {rst_type}')

        return Restaurant.objects \
            .prefetch_related('ratings', 'sales') \
            .filter(restaurant_type__iexact=rst_type)


class RestaurantUpdateAPIView(generics.UpdateAPIView):
    # this view is still not optimized
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        rst_id = self.kwargs['id']

        try:
            rest = Restaurant.objects.get(id=rst_id)

            if timezone.now().date() - rest.date_opened > timedelta(days=365):
                return rest
            else:
                return PermissionDenied(
                    detail='The requested restaurant has not been \
                            around for more than a year')

        except Restaurant.DoesNotExist:
            raise NotFound('Requested Restaurant does not exist')


class TopRestaurantsAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        rests = Restaurant.objects.prefetch_related('ratings', 'sales') \
            .annotate(avg_rating=Avg('ratings__rating')) \
            .order_by('-avg_rating')[:5]

        return rests


class AtLeastOneTopRateAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        rests = Restaurant.objects \
            .prefetch_related('ratings', 'sales') \
            .filter(ratings__rating=5)

        return rests


class ZeroRatingRestaurantsAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        rests = Restaurant.objects \
            .prefetch_related('ratings', 'sales') \
            .annotate(rat_count=Coalesce(Count('ratings__rating'), Value(0))) \
            .filter(rat_count__lt=1)

        return rests


class SpecialIncomInSpecialDayAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        date_str = self.kwargs['date']
        specific_date = date.fromisoformat(date_str)

        rests = Restaurant.objects \
            .prefetch_related('ratings', 'sales') \
            .filter(Q(sales__income__gt=5_000) &
                    Q(sales__datetime__date=specific_date))

        return rests


class UsersTopRatingResuaurant(generics.RetrieveAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(detail=f'User with id {user_id} does not exist')

        user_top_rating = user.rating_set.order_by('-rating').first()
        if not user_top_rating:
            raise NotFound(
                detail=f'No ratings found for the user with id {user_id}')
        return user_top_rating.restaurant


class AllSalesOfSpecificRestaurant(generics.ListAPIView):
    serializer_class = serializers.SaleSerializer
    permission_classes = [AllowAny]
    # pagination_class = LimitedResultsSetPagination

    def get_queryset(self):
        rst_id = self.kwargs['restaurant_id']

        try:
            restaurant = Restaurant.objects.get(id=rst_id)

        except Restaurant.DoesNotExist:
            raise NotFound(f'Restaurant with this id: {rst_id} not found')

        sales = Sale.objects.filter(restaurant=restaurant)

        return sales
