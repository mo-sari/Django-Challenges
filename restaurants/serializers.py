from restaurants.models import Restaurant, Rating, Sale

from rest_framework.serializers import ModelSerializer

from rest_framework.serializers import ValidationError
from django.db import IntegrityError


class RatingSerializer(ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        try:
            return super().create(validated_data)

        except IntegrityError:
            raise ValidationError('This user has already rated this restaurant')


class SaleSerializer(ModelSerializer):

    class Meta:
        model = Sale
        fields = '__all__'


class RestaurantSerializer(ModelSerializer):
    ratings = RatingSerializer(many=True)
    sales = SaleSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

    def validate_name(self, value):
        if not (value[0].isupper()):
            raise ValidationError(
                detail=f'The restaurant name provided ({value}) does not start with an upper case letter')

        return value
