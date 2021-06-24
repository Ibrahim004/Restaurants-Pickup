from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Restaurant, Menu, Customer, Location


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    field_order = ['username', 'email', 'password1', 'password2']


class RestaurantDetailsForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'opening_time', 'closing_time', 'genre']


class MenuDetailsForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'from_time', 'to_time']


class CustomerDetailsForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number']


class LocationDetailsForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['country', 'province', 'city', 'street_address', 'postal_code']
