from django.shortcuts import render
from django.http import HttpResponse
from .models import Restaurant, Menu


def index(request):
    return HttpResponse("Hello world. This is the main page for Foody!")


def get_restaurants(request):
    all_restaurants = Restaurant.objects.all()
    # return render(request, 'foodyapp/restaurants.html', {'list_of_restaurants': all_restaurants})
    return render(request, 'foodyapp/all_restaurants.html', {'restaurants': all_restaurants})


def get_restaurant_details(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(request, 'foodyapp/restaurant_details.html', {'restaurant': restaurant})


def get_menu_details(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    restaurant = menu.restaurant_set.all()[0]
    return render(request, 'foodyapp/menu_details.html', {'menu': menu, 'restaurant': restaurant})


# todo: implement function to handle post request for order review
def review_order(request):
    pass

# todo: implement function to submit order to restaurant

# todo: improve UI for listing all restaurants

# todo: add functionality to display restaurants sorted by distance

# todo: implement restaurant dashboard

# todo: implement customer dashboard
