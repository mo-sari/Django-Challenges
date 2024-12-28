from rest_framework import generics
from restaurants import serializers
from rest_framework.permissions import AllowAny
from restaurants.models import Restaurant
from rest_framework.exceptions import NotFound, ValidationError


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
