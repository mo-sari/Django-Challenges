from django.urls import path
from .views import RestaurantsAPIView, RestaurantAPIView


urlpatterns = [
    path('restaurants/', RestaurantsAPIView.as_view()),
    path('restaurant/<str:rst_name>/', RestaurantAPIView.as_view()),
]
