from django.urls import path
from .views import (
    RestaurantsAPIView,
    RestaurantAPIView,
    RestaurantByTypeAPIView,
    RestaurantUpdateAPIView)


urlpatterns = [
    path('restaurants/', RestaurantsAPIView.as_view()),
    path('restaurant/<str:rst_name>/', RestaurantAPIView.as_view()),
    path('restaurants/<str:rst_type>/', RestaurantByTypeAPIView.as_view()),
    path('restaurant-update/<int:id>/', RestaurantUpdateAPIView.as_view())
]
