from rest_framework import status
from rest_framework.response import Response

from django.utils import timezone
from datetime import datetime, timedelta, date

from rest_framework import generics
from restaurants import serializers
from rest_framework.permissions import AllowAny
from restaurants.models import Restaurant
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from django.db.models import Avg, Sum, Min, Max, Count, Value, Q, F
from django.db.models.functions import Coalesce


class RestaurantsAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]
    queryset = Restaurant.objects.all()


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

        return Restaurant.objects.filter(restaurant_type__iexact=rst_type)


class RestaurantUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        rst_id = self.kwargs['id']

        try:
            rest = Restaurant.objects.get(id=rst_id)
            if timezone.now() - rest.date_opened > timedelta(days=365):
                return rest
            else:
                return PermissionDenied(detail='The requested restaurant has not been around for more than a year')

        except Restaurant.DoesNotExist:
            raise NotFound('Requested Restaurant does not exist')


class TopRestaurantsAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        rests = Restaurant.objects.annotate(
            avg_rating=Avg('ratings__rating')).order_by('-avg_rating')[:5]
        return rests


class AtLeastOneTopRateAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        rests = Restaurant.objects.filter(ratings__rating__gte=5)
        return rests


class ZeroRatingRestaurantsAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        rests = Restaurant.objects.annotate(
            rat_count=Coalesce(Count('ratings__rating'), Value(0))).filter(
                rat_count__lt=1)
        return rests


class SpecialIncomInSpecialDayAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        date_str = self.kwargs['date']
        specific_date = date.fromisoformat(date_str)

        rests = Restaurant.objects.filter(
            Q(sales__income__gt=5_000) & Q(
                sales__datetime__date=specific_date))
        return rests
