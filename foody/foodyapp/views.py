from django.shortcuts import render
from django.http import HttpResponse
from .models import Restaurant


def index(request):
    return HttpResponse("Hello world. This is the main page for Foody!")


def get_restaurants(request):
    all_restaurants = Restaurant.objects.all()
    return render(request, 'foodyapp/restaurants.html', {'list_of_restaurants': all_restaurants})


def get_restaurant_details(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(request, 'foodyapp/restaurant_details.html', {'restaurant': restaurant})


def get_menu_details(request, menu_id):
    pass
