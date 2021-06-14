from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('restaurants/', views.get_restaurants, name='restaurants'),
    path('restaurants/signup/', views.restaurant_signup, name='restaurant_signup'),
    path('restaurants/signup/restaurant_info/', views.add_restaurant_info, name='restaurant_add_info'),
    path('restaurants/signup/menu_info', views.add_menu_info, name='restaurant_add_menu'),
    path('restaurant/login/', views.restaurant_login, name='restaurant_login'),
    path('restaurant_details/<str:restaurant_id>', views.get_restaurant_details, name='restaurant_details'),
    path('menu_details/<str:menu_id>', views.get_menu_details, name='menu_details'),
    path('submit_order/<int:restaurant_id>/<int:menu_id>/', views.submit_order, name='submit_order'),
    path('confirmation/', views.order_confirmation, name='order_confirmation'),

]