from django.urls import path
from .views import (
    RestaurantsAPIView,
    RestaurantAPIView,
    RestaurantByTypeAPIView,
    RestaurantUpdateAPIView,
    TopRestaurantsAPIView,
    AtLeastOneTopRateAPIView,
    ZeroRatingRestaurantsAPIView,
    SpecialIncomInSpecialDayAPIView,
    UsersTopRatingResuaurant,
    AllSalesOfSpecificRestaurant,
    CreateRatingAPIView,
    DeleteRatingAPIView,
    GetRatingAPIView,
    AllRatings,
    RestaurantAverageRating,
    RestaurantTotalIncomeOverDateRange
    )


urlpatterns = [
    path('restaurants/', RestaurantsAPIView.as_view()),
    path('restaurant/<str:rst_name>/', RestaurantAPIView.as_view()),
    path('restaurants/<str:rst_type>/', RestaurantByTypeAPIView.as_view()),
    path('restaurant-update/<int:id>/', RestaurantUpdateAPIView.as_view()),
    path('restaurants-top/', TopRestaurantsAPIView.as_view()),
    path('restaurants-rated-five/', AtLeastOneTopRateAPIView.as_view()),
    path('zero-rating-restaurants/', ZeroRatingRestaurantsAPIView.as_view()),
    path('income-in/<str:date>/',
         SpecialIncomInSpecialDayAPIView.as_view()),
    path('users-top-rating-restaurant/<int:user_id>/',
         UsersTopRatingResuaurant.as_view()),
    path('restaurants/<int:restaurant_id>/sales/',
         AllSalesOfSpecificRestaurant.as_view()),
    path('create-rating/', CreateRatingAPIView.as_view()),
    path('delete-rating/<int:rating_id>/', DeleteRatingAPIView.as_view()),
    path('get-rating/<int:rating_id>/', GetRatingAPIView.as_view()),
    path('get-rating/<int:rating_id>/', GetRatingAPIView.as_view()),
    path('all-ratings/', AllRatings.as_view()),

    path('restaurant/<int:rest_id>/average/',
         RestaurantAverageRating.as_view()),
    path('something/<int:rest_id>/', RestaurantTotalIncomeOverDateRange.as_view()),
]
