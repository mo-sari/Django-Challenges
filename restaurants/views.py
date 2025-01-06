from django.contrib.auth.models import User
from .models import Rating

from django.utils import timezone
from datetime import timedelta, date

from restaurants import serializers
from restaurants.models import Restaurant, Sale
from restaurants.paginations import LimitedResultsSetPagination

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.exceptions import (
    NotFound,
    ValidationError,
    PermissionDenied)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count, Value, Q, Sum
from django.db.models.functions import Coalesce
# from django.db import connection
# from pprint import pprint


class RestaurantsAPIView(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [AllowAny]

    # pagination_class = LimitedResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'restaurant_type']
    filterset_fields = ['ratings__rating', 'date_opened']

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
        print(self.request.query_params)
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


class CreateRatingAPIView(APIView):
    serializers_class = serializers.RatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = self.serializers_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DeleteRatingAPIView(APIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):

        try:
            rating_id = self.kwargs['rating_id']
            rating = Rating.objects.get(id=rating_id)

            rating.delete()
            return Response(
                {'item successfully deleted'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Rating.DoesNotExist:
            return Response(
                {'error': f' request rating with id: {rating_id} \
                 was not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class GetRatingAPIView(APIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        try:
            rating_id = self.kwargs['rating_id']
            rating = Rating.objects.get(id=rating_id)

            serialized_rating = self.serializer_class(rating)
            return Response(
                serialized_rating.data,
                status=status.HTTP_200_OK
            )
        except Rating.DoesNotExist:
            return Response(
                {'error':
                 f'requested rating with id: {rating_id} was not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class AllRatings(APIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        ratings = Rating.objects.all()
        serialized_data = self.serializer_class(ratings, many=True)

        return Response(
            serialized_data.data,
            status=status.HTTP_200_OK
            )


class RestaurantAverageRating(APIView):
    serializer_class = serializers.RestaurantAvgRatingSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            rest_id = self.kwargs['rest_id']

            # restaurant = Restaurant.objects.prefetch_related('ratings') \
            #                                .get(id=rest_id)

            # ratings_avg = restaurant.ratings.aggregate(
            #     avg_rating=Avg('rating'))

            # return Response(
            #     ratings_avg,
            #     status=status.HTTP_200_OK
            # )

            restaurant = Restaurant.objects.prefetch_related('ratings') \
                                           .values('name', 'id') \
                                           .annotate(
                                               avg_rating=Avg(
                                                   'ratings__rating')) \
                                           .get(id=rest_id)

            return Response(
                restaurant['avg_rating'],
                status=status.HTTP_200_OK
            )
        except Restaurant.DoesNotExist:
            return Response(
                {'error': f'Restaurant with id: ({id}) does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
