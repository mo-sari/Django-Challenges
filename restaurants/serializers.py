from restaurants.models import Restaurant, Rating, Sale
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from rest_framework.serializers import ValidationError
from django.db import IntegrityError


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class RatingSerializer(ModelSerializer):
    user = UserSerializer(many=False)

    def get_restaurant_rating_count(self, obj):
        return obj.restaurant_rating_count()

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        try:
            return super().create(validated_data)

        except IntegrityError:
            raise ValidationError(
                'This user has already rated this restaurant'
                )


class SaleSerializer(ModelSerializer):

    class Meta:
        model = Sale
        fields = '__all__'


class RestaurantSerializer(ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    sales = SaleSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

    def validate_name(self, value):
        if not (value[0].isupper()):
            raise ValidationError(
                detail=f'The restaurant name provided ({value}) does not start with an upper case letter')

        return value


class RestaurantAvgRatingSerializer(serializers.Serializer):
    avg_rating = serializers.DecimalField(
        max_digits=5,
        decimal_places=2
    )


class RestaurantStatistics(serializers.Serializer):
    sales_count = serializers.IntegerField()
    total_income = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    avg_rating = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
