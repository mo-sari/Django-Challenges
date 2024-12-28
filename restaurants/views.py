from rest_framework import generics
from restaurants import serializers
from rest_framework.permissions import AllowAny
from restaurants.models import Restaurant


class RestaurantsAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]
    queryset = Restaurant.objects.all()

    # def get_queryset(self):

    #     query_set = self.queryset
    #     query_set.annotate()
