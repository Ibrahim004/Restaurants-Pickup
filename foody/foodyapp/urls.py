from django.urls import path
from . import views
from . import customer_views

urlpatterns = [
    path('', views.index, name='main'),
    path('restaurants/', views.get_restaurants, name='restaurants'),
    path('restaurants/signup/', views.restaurant_signup, name='restaurant_signup'),
    path('restaurants/signup/restaurant_info/', views.add_restaurant_info, name='restaurant_add_info'),
    path('restaurants/signup/menu/add/', views.add_menu_info, name='restaurant_add_menu'),
    path('restaurants/signup/menu/<int:menu_id>/item/add/', views.add_food_items, name='add_food_items'),
    path('restaurants/signup/menu/<int:menu_id>/success/', views.show_menu, name='successfully_added_menu'),
    path('restaurants/login/', views.login_view, name='restaurant_login'),
    path('restaurants/logout/', views.user_logout, name='restaurant_logout'),
    path('restaurants/main/', views.restaurant_main, name='restaurant_main_page'),
    path('restaurant_details/<str:restaurant_id>', views.get_restaurant_details, name='restaurant_details'),
    path('menu_details/<str:menu_id>', views.get_menu_details, name='menu_details'),
    path('submit_order/<int:restaurant_id>/<int:menu_id>/', views.submit_order, name='submit_order'),
    path('confirmation/', views.order_confirmation, name='order_confirmation'),
    path('customer/signup/', customer_views.signup, name='customer_signup'),
    path('customer/signup/info/', customer_views.add_info, name='add_customer_info'),
    path('customer/signup/location/', customer_views.add_location, name='add_customer_location'),
    path('customer/login/', views.login_view, name='customer_login'),
    path('customer/login/success/', customer_views.main, name='customer_login_success'),
    path('customer/logout/', views.user_logout, name='customer_logout'),
]