from django.test import TestCase
from .models import *
from datetime import time
from django.shortcuts import reverse
from django.contrib.auth.forms import UserCreationForm


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


class RestaurantModelTest(TestCase):

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

    def test_can_create_customer_with_user(self):
        pass


class RestaurantSignUpTest(TestCase):

    def test_can_get_restaurant_signup_form_with_correct_fields(self):
        response = self.client.get(reverse('restaurant_signup'))

        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertIsNotNone(form)

        self.assertTrue(isinstance(form, UserCreationForm))
        self.assertIsNotNone(form.fields['email'])

    def test_can_create_account_using_restaurant_signup_view(self):
        user = {'username': 'john1234', 'email': 'example@example.com', 'password1': 'mnbg1045',
                'password2': 'mnbg1045'}

        response = self.client.post(reverse('restaurant_signup'), user)

        self.assertEqual(response.status_code, 302)

    def test_can_get_restaurant_info_form(self):
        response = self.client.get(reverse('restaurant_add_info'))
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertIsNotNone(form)

        all_fields = ['name', 'address', 'opening_time', 'closing_time', 'genre']

        self.assertEqual(all_fields, form.Meta.fields)
