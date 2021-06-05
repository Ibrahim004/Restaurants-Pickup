

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('restaurants/', views.get_restaurants, name='restaurants'),
    path('restaurant_details/<str:restaurant_id>', views.get_restaurant_details, name='restaurant_details'),
    path('menu_details/<str:menu_id>', views.get_menu_details, name='menu_details'),
    path('review_order/<str:restaurant_id>/<str:menu_id>', views.review_order, name='review_order'),
    path('submit_order/<str:restaurant_id>/', views.submit_order, name='submit_order'),
]