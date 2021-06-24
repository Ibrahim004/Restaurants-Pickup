from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from .forms import SignUpForm, CustomerDetailsForm, LocationDetailsForm
from .models import Customer

from django.shortcuts import render, reverse
from django.contrib.auth import login, logout


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('restaurants'))

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            # login user
            login(request, user)

            return HttpResponseRedirect(reverse('add_customer_info'))
    else:
        form = SignUpForm()

    return render(request, 'foodyapp/customer_signup.html', {'form': form})


@login_required()
def add_info(request):
    user = request.user

    if request.method == 'POST':
        form = CustomerDetailsForm(request.POST)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = user
            customer.save()

            return HttpResponseRedirect(reverse('add_customer_location'))
    else:
        form = CustomerDetailsForm()
    return render(request, 'foodyapp/customer_details.html', {'form': form})


@login_required()
def add_location(request):
    user = request.user

    if not Customer.objects.filter(user=user).exists():
        return HttpResponseRedirect(reverse('add_customer_info'))

    customer = Customer.objects.get(user=user)

    if request.method == 'POST':
        form = LocationDetailsForm(request.POST)

        if form.is_valid():
            location = form.save()
            customer.location = location
            customer.save()

            return HttpResponseRedirect(reverse('restaurants'))

    else:
        form = LocationDetailsForm()

    return render(request, 'foodyapp/customer_location.html', {'form': form})


def customer_login(request):
    pass
