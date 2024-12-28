from django.urls import path
from .views import RestaurantsAPIView


urlpatterns = [
    path('restaurants/', RestaurantsAPIView.as_view()),
]
