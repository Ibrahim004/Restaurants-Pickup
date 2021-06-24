from django.test import TestCase

from django.shortcuts import reverse
from django.contrib.auth.models import User

from .forms import SignUpForm
from .models import Customer, Location


class CustomerSignUpTests(TestCase):

    def create_user(self):
        self.user_username = 'user1'
        self.user_password = 'userpassword5384384'
        self.user = User.objects.create_user(username=self.user_username, password=self.user_password)

    def setUp(self) -> None:
        self.create_user()

        self.customer_phone_number = '111-222-3333'
        self.customer_details = {'first_name': 'John', 'last_name': 'Doe', 'phone_number': self.customer_phone_number}

    def test_can_get_signup_page(self):
        response = self.client.get(reverse('customer_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response.context['form']) == SignUpForm)

    def test_if_user_is_logged_in_signup_should_redirect_to_main_page(self):
        # login user
        did_login = self.client.login(username=self.user_username, password=self.user_password)
        self.assertTrue(did_login)

        response = self.client.get(reverse('customer_signup'))
        self.assertRedirects(response, reverse('restaurants'))

    def test_should_be_able_to_signup_new_user(self):
        password = 'complexPassword23848'
        username = 'user2'
        user = {'username': username, 'email': 'user@example.com', 'password1': password,
                'password2': password}
        response = self.client.post(reverse('customer_signup'), data=user)
        self.assertRedirects(response, reverse('add_customer_info'))

        retrieved_user = User.objects.get(username=username)
        self.assertIsNotNone(retrieved_user)

    def test_should_be_able_to_add_customer_info(self):
        # login user
        did_login = self.client.login(username=self.user_username, password=self.user_password)
        self.assertTrue(did_login)

        # post customer details

        response = self.client.post(reverse('add_customer_info'), data=self.customer_details)
        self.assertRedirects(response, reverse('add_customer_location'))

        # check that customer details were added to db
        customer = Customer.objects.get(phone_number=self.customer_phone_number)
        self.assertIsNotNone(customer)

        # check that user was assigned to customer
        self.assertTrue(customer.user == self.user)

    def test_should_be_able_to_add_location_info(self):
        # login user
        did_login = self.client.login(username=self.user_username, password=self.user_password)
        self.assertTrue(did_login)

        # create customer
        response = self.client.post(reverse('add_customer_info'), self.customer_details)
        self.assertRedirects(response, reverse('add_customer_location'))

        # post location details
        postal_code = 'R3C 4A5'
        location_details = {'country': 'Canada', 'province': 'MB', 'city': 'Winnipeg',
                            'street_address': '1234 Some Street', 'postal_code': postal_code}
        response = self.client.post(reverse('add_customer_location'), data=location_details)
        self.assertRedirects(response, reverse('restaurants'))

        # check location was added to db
        retrieved_customer = Customer.objects.get(phone_number=self.customer_phone_number)
        retrieved_location = Location.objects.get(postal_code=postal_code)
        self.assertTrue(retrieved_customer.location == retrieved_location)

    def test_location_invalid_postal_code_should_return_error(self):
        pass

    def test_customer_phone_number_should_be_valid_format(self):
        pass


