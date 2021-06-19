from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Restaurant, Menu, FoodItem


class RestaurantSignUpForm(UserCreationForm):
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
