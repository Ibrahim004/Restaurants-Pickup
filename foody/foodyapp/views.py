from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden

from .exceptions import FieldFormatIncorrect
from .models import Restaurant, Menu, Order, FoodItem, Customer, RestaurantTaxRate, OrderFoodItem
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import SignUpForm, RestaurantDetailsForm, MenuDetailsForm


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


# order_items is a dictionary with food_item and quantity
def _calculate_subtotal(order_items):
    sub_total = 0
    for item in order_items:
        sub_total += (item.quantity * item.food_item.price)
    # for item, quantity in order_items.items():
    #     sub_total += item.price * quantity
    return sub_total


# adds tax on order based on restaurant location
def _get_total(location, subtotal):
    province = location.province
    tax_rate = RestaurantTaxRate.tax_rate[province]
    return subtotal * (1 + float(tax_rate)/100.0)


# set the food_items property on order object using keys from order_items dictionary
def _set_items(order, order_items):
    order.items.set(order_items)
    order.save()


# returns the list of OrderFoodItem elements
def _get_order_items(menu, data):
    # order_items = dict()
    order_items = []
    for food_item in menu.fooditem_set.all():
        count = int(data[food_item.name])
        if count > 0:
            item = OrderFoodItem(quantity=count, food_item=food_item)
            item.save()
            order_items.append(item)
            # order_items[food_item] = count
    return order_items


def submit_order(request, restaurant_id, menu_id):
    # take order details
    menu = Menu.objects.get(id=menu_id)
    restaurant = Restaurant.objects.get(id=restaurant_id)

    # get the items from post data
    order_items = _get_order_items(menu, request.POST)

    # calculate subtotal
    subtotal = _calculate_subtotal(order_items)

    # calculate total
    total = _get_total(restaurant.location, subtotal)

    # create an order record
    order = Order(restaurant=restaurant, order_total=total)
    order.save()
    _set_items(order, order_items)

    # todo: send order details to restaurant

    # todo: send confirmation to customer
    return HttpResponseRedirect(reverse('order_confirmation'))


# todo: add functionality to display restaurants sorted by distance

# todo: implement restaurant dashboard

# todo: implement customer dashboard

def order_confirmation(request):
    return HttpResponse("Your order was submitted!")


def restaurant_signup(request):
    if request.method == 'POST':
        # take the post data and validate it
        form = SignUpForm(request.POST)

        if form.is_valid():
            # sign the user up for an account
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                            form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('restaurant_add_info'))

    else:
        form = SignUpForm()

    return render(request, 'foodyapp/restaurant_signup.html', {'form': form})


# redirect user after logging in based on user type
# user can be either restaurant or customer user for now (25/06/2021)
def _get_redirect_path(user):
    if Restaurant.objects.filter(user=user).exists():
        return reverse('restaurant_main_page')
    elif Customer.objects.filter(user=user).exists():
        return reverse('customer_login_success')
    else:
        assert False


def _get_template_path(path):
    if 'restaurant' in path:
        return 'foodyapp/restaurant_login.html'
    elif 'customer' in path:
        return 'foodyapp/customer_login.html'
    else:
        assert False


def login_view(request):
    user = request.user
    if user.is_authenticated:
        # redirect based on user type
        redirect_path = _get_redirect_path(user)
        return HttpResponseRedirect(redirect_path)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # redirect based on user type
                redirect_path = _get_redirect_path(user)
                return HttpResponseRedirect(redirect_path)
    else:
        form = AuthenticationForm()

    template_path = _get_template_path(request.path)
    return render(request, template_path, {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'foodyapp/logout_success.html')


@login_required()
def add_restaurant_info(request):
    user = request.user

    if request.method == 'POST':
        form = RestaurantDetailsForm(request.POST)

        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.user = user
            restaurant.save()

            return HttpResponseRedirect(reverse('restaurant_add_menu'))

    else:
        form = RestaurantDetailsForm()

    return render(request, 'foodyapp/restaurant_info_form.html', {'form': form, 'user': user})


@login_required()
def add_menu_info(request):
    user = request.user
    restaurant = Restaurant.objects.get(user=user)

    if request.method == 'POST':
        form = MenuDetailsForm(request.POST)

        if form.is_valid():
            menu = form.save()
            restaurant.menus.add(menu)
            restaurant.save()

            return HttpResponseRedirect(reverse('add_food_items', args=(menu.id,)))
    else:
        form = MenuDetailsForm()

    return render(request, 'foodyapp/add_menu.html', {'form': form, 'user': user})


@login_required()
def add_food_items(request, menu_id):
    user = request.user
    restaurant = Restaurant.objects.get(user=user)

    if restaurant.menus.filter(id=menu_id).exists():
        menu = Menu.objects.get(id=menu_id)
        if request.method == 'POST':
            _add_food_items_to_database(request.POST, menu)

            return HttpResponseRedirect(reverse('successfully_added_menu', args=(menu.id,)))

        return render(request, 'foodyapp/add_food_items.html', {'user': user, 'menu': menu})
    else:
        return HttpResponseForbidden()


@login_required()
def show_menu(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    return render(request, 'foodyapp/menu_details.html', {'menu': menu})


def _add_food_items_to_database(data_dict, menu):
    name = ''
    description = ''
    price = -1

    for key in data_dict:

        if key.startswith('food_item_name'):
            name = data_dict[key]
        if key.startswith('food_item_description'):
            description = data_dict[key]
        if key.startswith('food_item_price'):
            price = data_dict[key]

        if name != '' and description != '' and price != -1:
            item = FoodItem(name=name, description=description, price=price)
            item.save()
            item.menu = menu

            # reset all input variables
            name = ''
            description = ''
            price = -1


def restaurant_main(request):
    return HttpResponse("You have logged in successfully")
    pass
