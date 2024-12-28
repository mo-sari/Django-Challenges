from restaurants.models import Restaurant, Rating, Sale
from rest_framework.serializers import ModelSerializer


class RatingSerializer(ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'


class RestaurantSerializer(ModelSerializer):
    ratings = RatingSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class SaleSerializer(ModelSerializer):

    class Meta:
        model = Sale
        fields = '__all__'
