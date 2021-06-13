from django import forms
from django.contrib.auth.forms import UserCreationForm


class RestaurantSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    field_order = ['username', 'email', 'password1', 'password2']
