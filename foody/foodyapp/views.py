from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Restaurant, Menu, Order


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

    try:
        restaurant = menu.restaurant_set.first()
    except IndexError:
        return render(request, 'foodyapp/menu_details2.html', {'menu': menu})

    return render(request, 'foodyapp/menu_details2.html', {'menu': menu, 'restaurant': restaurant})


# def review_order(request, restaurant_id, menu_id):
#     context = {'restaurant_name': '', 'list_of_items': [{'name': '', 'quantity': '', 'price': ''}]}
#     restaurant_name = Restaurant.objects.get(id=restaurant_id).name
#     menu = Menu.objects.get(id=menu_id)
#
#     list_of_items = []
#     print(request.POST.keys())
#
#     for item in menu.fooditem_set.all():
#         quantity = request.POST.get(item.id)
#
#         if quantity > 0:
#             list_item = {'name': item.name, 'quantity': quantity, 'price': (quantity * item.price)}
#             list_of_items.append(list_item)
#
#     context['restaurant_name'] = restaurant_name
#     context['list_of_items'] = list_of_items
#
#     return render(request, 'foodyapp/order_details.html', context)


def submit_order(request, restaurant_id, menu_id):
    # take order details
    menu = Menu.objects.get(id=menu_id)
    restaurant = Restaurant.objects.get(id=restaurant_id)

    items = []
    quantity = []

    for fooditem in menu.fooditem_set.all():
        count = int(request.POST[fooditem.name])
        if count > 0:
            items.append(fooditem)
            quantity.append(count)

    # calculate subtotal
    subtotal = 0
    for i in range(len(items)):
        subtotal += (items[i].price * quantity[i])

    # create an order record
    order = Order(restaurant=restaurant, order_total=subtotal)
    order.save()
    order.food_items.set(items)
    order.save()

    # todo: send order details to restaurant

    # todo: send confirmation to customer
    return HttpResponseRedirect(reverse('order_confirmation'))


# todo: add functionality to display restaurants sorted by distance

# todo: implement restaurant dashboard

# todo: implement customer dashboard

def order_confirmation(request):
    return HttpResponse("Your order was submitted!")
