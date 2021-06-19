from django.test import TestCase, Client
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

    def setUp(self) -> None:
        self.create_user()

    def create_user(self):
        self.user_password = 'password283838'
        self.user_username = 'user1'
        self.user = User.objects.create_user(username=self.user_username, email='email@example.com', password=self.user_password)

    def create_restaurant(self, user):
        self.restaurant = Restaurant.objects.create(name='Great Value Restaurant', opening_time=time(hour=6),
                                                    closing_time=time(hour=18),
                                                    address='1234 Main Way, City, Province, Country', user=user)

    def create_menu(self, restaurant):
        self.menu = Menu.objects.create(title="Great Value Menu", from_time=time(hour=6), to_time=time(hour=21))
        self.menu.restaurant_set.add(restaurant)

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

        retrieved_user = User.objects.get(username=user['username'])

        self.assertIsNotNone(retrieved_user)
        self.assertEqual(response.status_code, 302)

    def test_can_get_restaurant_info_form(self):
        login_was_successful = self.client.login(username=self.user_username, password=self.user_password)

        self.assertTrue(login_was_successful)

        response = self.client.get(reverse('restaurant_add_info'))
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertIsNotNone(form)

        all_fields = ['name', 'address', 'opening_time', 'closing_time', 'genre']

        self.assertEqual(all_fields, form.Meta.fields)

    def test_restaurant_has_user_assigned_after_submitting_details(self):
        restaurant_details = {'name': 'Great Value Restaurant', 'address': '1234 CityRoad, City, Province, Postal Code',
                              'opening_time': time(hour=6), 'closing_time': time(hour=23), 'genre': 'BRK'}

        login_was_successful = self.client.login(username=self.user_username, password=self.user_password)

        self.assertTrue(login_was_successful)

        response = self.client.post(reverse('restaurant_add_info'), restaurant_details)

        self.assertEqual(response.status_code, 302)

        restaurant = Restaurant.objects.get(name=restaurant_details['name'])
        self.assertIsNotNone(restaurant)
        self.assertIsNotNone(restaurant.user)

    def test_menu_is_added_to_restaurant_after_submitting_menu_details(self):
        # create a restaurant to contain the menu
        self.create_restaurant(self.user)

        # the details that will be submitted to the menu form
        menu_details = {'title': "Great Value Menu", 'from_time': time(hour=6), 'to_time': time(hour=18)}

        # login the user
        login_was_successful = self.client.login(username=self.user_username, password=self.user_password)
        self.assertTrue(login_was_successful)

        # submit the menu details
        response = self.client.post(reverse('restaurant_add_menu'), menu_details)

        # check we are redirected after successfully submitting the menu
        self.assertEqual(response.status_code, 302)

        # check the menu has a restaurant associated with it
        menu = Menu.objects.get(title=menu_details['title'])
        self.assertEqual(menu.restaurant_set.count(), 1)

    def test_restaurant_should_only_be_able_to_edit_its_menu(self):
        # login user
        did_login = self.client.login(username=self.user_username, password=self.user_password)
        self.assertTrue(did_login)

        # create restaurant and menu
        self.create_restaurant(self.user)
        self.create_menu(self.restaurant)

        # we should be able to edit the menu for our restaurant
        food_items = {'food_item_name0': 'Fries', 'food_item_description0': 'great fries', 'food_item_price0': '2.99',
                      'food_item_name1': 'Burger', 'food_item_description1': 'great burger', 'food_item_price1': '4.99'}
        response = self.client.post(reverse('add_food_items', args=(self.menu.id,)), food_items)
        self.assertEqual(response.status_code, 302)

        # we should not be able to edit the menu for another restaurant
        response = self.client.post(reverse('add_food_items', args=(100,)), food_items)
        self.assertEqual(response.status_code, 403)

    def test_should_return_error_if_submitting_food_items_in_wrong_format(self):
        pass

    def test_should_be_able_to_get_food_items_page(self):
        pass

    def test_should_be_able_to_add_items_to_menu(self):
        pass
