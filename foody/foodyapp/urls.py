

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('restaurants/', views.get_restaurants, name='restaurants'),
    path('restaurant_details/<str:restaurant_id>', views.get_restaurant_details, name='restaurant_details'),
]