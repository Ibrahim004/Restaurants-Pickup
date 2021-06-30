from django.test import TestCase
from .models import Restaurant, Menu, FoodItem, Order, Location, Customer, OrderFoodItem
from django.shortcuts import reverse
from datetime import time


# helper functions to create mockup data for tests
def create_restaurant_location():
    restaurant_location = Location.objects.create(country='Canada', province='BC', city='New Westminster',
                                                  street_address='514 8th Ave', postal_code='V3L 2Y3')
    return restaurant_location


def create_customer_location():
    customer_location = Location.objects.create(country='Canada', province='BC', city='Vancouver',
                                                street_address='1234 W Broadway', postal_code='V6T 1Z4')
    return customer_location


def create_customer():
    customer_location = create_customer_location()
    customer = Customer.objects.create(first_name="John", last_name="Doe", location=customer_location,
                                       phone_number='123-456-7900')
    return customer


def create_restaurant():
    restaurant_location = create_restaurant_location()
    restaurant_menu = create_restaurant_menu()

    restaurant = Restaurant(name="iHop", opening_time=time(hour=7), closing_time=time(hour=20),
                            address='514 8th Ave, New Westminster, BC V3L 2Y3',
                            location=restaurant_location, genre='Breakfast')
    restaurant.save()
    restaurant.menus.add(restaurant_menu)
    restaurant.save()

    return restaurant


def create_restaurant_menu():
    restaurant_menu = Menu.objects.create(title='All Day Breakfast', from_time=time(hour=7),
                                          to_time=time(hour=20))

    pancakes = FoodItem(name='Pancakes', description='World famous pancakes', price=12.99,
                        menu=restaurant_menu)
    pancakes.save()
    burger = FoodItem(name='Burger', description='We have burgers now', price=5.99, menu=restaurant_menu)
    burger.save()

    return restaurant_menu


class OrderTest(TestCase):

    def setUp(self) -> None:
        self.restaurant = create_restaurant()
        self.customer = create_customer()

    # adds the price for all food_items and returns it
    def _get_subtotal(self, food_items):
        subtotal = 0
        for item in food_items:
            subtotal += item.price
        return subtotal

    def test_can_create_order_and_get_total(self):
        order = Order(restaurant=self.restaurant, customer=self.customer, order_total=0)
        order.save()

        # order everything from the restaurant
        food_items = self.restaurant.menus.first().fooditem_set.all()
        order_food_items = [OrderFoodItem.objects.create(quantity=1, food_item=item) for item in food_items]
        order.items.set(order_food_items)

        total = self._get_subtotal(food_items)

        order.order_total = total
        order.save()

        retrieved_order = Order.objects.get(id=order.id)
        self.assertEquals(retrieved_order, order)
        self.assertTrue(retrieved_order.order_total > 0)


class ViewTest(TestCase):

    def test_can_get_menu_details(self):
        menu = create_restaurant_menu()
        response = self.client.get(reverse('menu_details', args=(menu.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['menu'])

    def test_can_get_menu_details_with_restaurant_details(self):
        restaurant = create_restaurant()
        menu = restaurant.menus.first()
        response = self.client.get(reverse('menu_details', args=(menu.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['menu'])
        self.assertIsNotNone(response.context['restaurant'])

    def test_submit_order_should_create_new_order(self):
        restaurant = create_restaurant()
        menu = restaurant.menus.first()
        item_quantity = dict()

        # order 2 of each item on menu
        total = 0
        for fooditem in menu.fooditem_set.all():
            item_quantity[fooditem.name] = 2
            total += (2 * fooditem.price)

        # todo: total calculation should reflect the restaurant location
        total *= 1.05

        response = self.client.post(reverse('submit_order', args=(restaurant.id, menu.id,)), item_quantity)

        # check we are redirected correctly
        self.assertEqual(response.status_code, 302)

        order = Order.objects.get(restaurant=restaurant)

        # check order was created in the database
        self.assertIsNotNone(order)

        # check all items were added
        all_items = order.items.all()
        all_food_items = [item.food_item for item in all_items]
        for item in menu.fooditem_set.all():
            self.assertTrue(item in all_food_items)

        # check that total is correct
        self.assertEqual(total, order.order_total)
