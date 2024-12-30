from django.urls import path
from .views import (
    RestaurantsAPIView,
    RestaurantAPIView,
    RestaurantByTypeAPIView,
    RestaurantUpdateAPIView,
    TopRestaurantsAPIView,
    AtLeastOneTopRateAPIView,
    ZeroRatingRestaurantsAPIView,
    SpecialIncomInSpecialDayAPIView)


urlpatterns = [
    path('restaurants/', RestaurantsAPIView.as_view()),
    path('restaurant/<str:rst_name>/', RestaurantAPIView.as_view()),
    path('restaurants/<str:rst_type>/', RestaurantByTypeAPIView.as_view()),
    path('restaurant-update/<int:id>/', RestaurantUpdateAPIView.as_view()),
    path('restaurants-top/', TopRestaurantsAPIView.as_view()),
    path('at-least-one-top-rate/', AtLeastOneTopRateAPIView.as_view()),
    path('zero-rating-restaurants/', ZeroRatingRestaurantsAPIView.as_view()),
    path('special-income-in-special-dates/<str:date>/',
         SpecialIncomInSpecialDayAPIView.as_view()),
]
