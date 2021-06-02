from django.test import TestCase
from .models import *
from datetime import time


class LocationTest(TestCase):

    def test_can_create_Location(self):
        dennys = Location(country="Canada", city='Vancouver', province='BC', streetAddress='1759 W Broadway',
                          postal_code='V6J 1Y2')
        dennys.save()
        retrieved_location = Location.objects.get(id=dennys.id)
        self.assertEquals(dennys, retrieved_location)


class MenuTest(TestCase):

    def test_can_create_a_new_menu(self):
        all_day_breakfast_menu = Menu(title="All Day Breakfast", from_time=time(hour=7), to_time=time(hour=23))
        all_day_breakfast_menu.save()
        retrieved_menu = Menu.objects.get(id=all_day_breakfast_menu.id)
        self.assertEquals(all_day_breakfast_menu, retrieved_menu)


class FoodItemTest(TestCase):

    def setUp(self) -> None:
        Menu.objects.create(title='All Day Breakfast', from_time=time(hour=7), to_time=time(hour=23))
        Menu.objects.create(title='Dinner Menu', from_time=time(hour=18), to_time=time(hour=23))

    def test_can_create_breakfast_foodItems(self):
        breakfast_menu = Menu.objects.get(title='All Day Breakfast')

        egg_omelette = FoodItem(name='Egg omelette', description='Delicious egg omelette with potatoes and sausage',
                                price=11.99, menu=breakfast_menu)
        egg_omelette.save()

        retrieved_omelette = FoodItem.objects.get(name='Egg omelette')
        self.assertEquals(egg_omelette, retrieved_omelette)

    def test_can_create_multiple_dinner_food_items(self):
        dinner_menu = Menu.objects.get(title='Dinner Menu')
        breakfast_menu = Menu.objects.get(title='All Day Breakfast')

        meatball_pasta = FoodItem(name='Meatballs Pasta', description='Italian style meatball pasta',
                                  price=22.5, menu=dinner_menu)
        meatball_pasta.save()
        vegetarian_pizza = FoodItem(name='5 veggie pizza', description='Vegetarian pizza with  '
                                                                       'tomatoes, spinach, mushrooms, '
                                                                       'green peppers, and pine apple',
                                    price=18.5, menu=dinner_menu)
        vegetarian_pizza.save()

        all_food_items = FoodItem.objects.all()
        self.assertEquals(all_food_items.count(), 2)
        self.assertEquals(dinner_menu.fooditem_set.all().count(), 2)


class RestaurantTest(TestCase):

    def setUp(self) -> None:
        self.location = Location.objects.create(country='Canada', province='British Columbia', city='Vancouver',
                                                streetAddress='1759 W Broadway', postal_code='V6J 1Y2')
        self.breakfast_menu = Menu.objects.create(title='All Day Breakfast', from_time=time(hour=7),
                                                  to_time=time(hour=23))

        self.eggs = FoodItem.objects.create(name='Eggs', description='world famous eggs with 2 biscuits', price=5.99,
                                            menu=self.breakfast_menu)
        self.pancakes = FoodItem.objects.create(name='Pancakes', description='Chocolate chip pancakes', price=7.95,
                                                menu=self.breakfast_menu)

    def test_can_create_a_restaurant(self):
        dennys = Restaurant(name='Denny\'s Restaurant', opening_time=time(hour=7), closing_time=time(hour=23),
                            address='1759 W Broadway, Vancouver, BC, V6J 1Y2', location=self.location, genre='FST')
        dennys.save()
        dennys.menus.add(self.breakfast_menu)

        retrieved_restaurant = Restaurant.objects.get(id=dennys.id)
        self.assertEquals(dennys, retrieved_restaurant)

        # test whether menus contain breakfast_menu
        self.assertIsNotNone(dennys.menus.filter(id=self.breakfast_menu.id))


class CustomerTest(TestCase):

    def setUp(self) -> None:
        self.location = Location.objects.create(country='Canada', province='BC', city='Vancouver',
                                                postal_code='V6T 1Z4', streetAddress='1234 W Broadway')

    def test_can_create_customer(self):
        customer = Customer(first_name='John', last_name='Doe', location=self.location, phone_number='604-123-4567')
        customer.save()

        retrieved_customer = Customer.objects.get(id=customer.id)
        self.assertEquals(customer, retrieved_customer)


class OrderTest(TestCase):

    def setUp(self) -> None:
        self.create_restaurant()
        self.create_customer()

    def test_can_create_order_and_get_total(self):
        order = Order(restaurant=self.restaurant, customer=self.customer, order_total=0)
        order.save()

        # order everything from the restaurant
        food_items = self.restaurant.menus.all()[0].fooditem_set.all()
        order.food_items.set(food_items)

        total = 0
        for item in food_items:
            total += item.price

        order.order_total = total
        order.save()

        retrieved_order = Order.objects.get(id=order.id)
        self.assertEquals(retrieved_order, order)
        self.assertTrue(retrieved_order.order_total > 0)

    def create_restaurant(self):
        self.create_restaurant_location()
        self.create_restaurant_menu()

        self.restaurant = Restaurant(name="iHop", opening_time=time(hour=7), closing_time=time(hour=20),
                                     address='514 8th Ave, New Westminster, BC V3L 2Y3',
                                     location=self.restaurant_location, genre='Breakfast')
        self.restaurant.save()
        self.restaurant.menus.add(self.restaurant_menu)
        self.restaurant.save()

    def create_customer(self):
        self.create_customer_location()
        self.customer = Customer.objects.create(first_name="John", last_name="Doe", location=self.customer_location,
                                                phone_number='123-456-7900')

    def create_customer_location(self):
        self.customer_location = Location.objects.create(country='Canada', province='BC', city='Vancouver',
                                                         streetAddress='1234 W Broadway', postal_code='V6T 1Z4')

    def create_restaurant_location(self):
        self.restaurant_location = Location.objects.create(country='Canada', province='BC', city='New Westminster',
                                                           streetAddress='514 8th Ave', postal_code='V3L 2Y3')

    def create_restaurant_menu(self):
        self.restaurant_menu = Menu.objects.create(title='All Day Breakfast', from_time=time(hour=7),
                                                   to_time=time(hour=20))

        pancakes = FoodItem(name='Pancakes', description='World famous pancakes', price=12.99,
                            menu=self.restaurant_menu)
        pancakes.save()

        burger = FoodItem(name='Burger', description='We have burgers now', price=5.99, menu=self.restaurant_menu)
        burger.save()
