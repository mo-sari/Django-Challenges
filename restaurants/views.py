from rest_framework import generics
from restaurants import serializers
from rest_framework.permissions import AllowAny
from restaurants.models import Restaurant
from rest_framework.exceptions import NotFound


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
