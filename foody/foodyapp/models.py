from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Restaurant(models.Model):
    # todo: add rating for restaurant
    RESTAURANT_TYPE = [('ITL', 'Italian'),
                       ('JPN', 'Japanese'),
                       ('IND', 'Indian'),
                       ('FST', 'Fast Food'),
                       ('SHI', 'Sushi'),
                       ('CHN', 'Chinese'),
                       ('BRK', 'Breakfast')]

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    address = models.CharField(max_length=200)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    genre = models.CharField(max_length=3, choices=RESTAURANT_TYPE, blank=True, null=True)
    menus = models.ManyToManyField('Menu')

    def __str__(self):
        return self.name


class Location(models.Model):
    CANADIAN_PROVINCES = [('BC', 'British Columbia'),
                          ('AB', 'Alberta'),
                          ('MB', 'Manitoba'),
                          ('NB', 'New Brunswick'),
                          ('NL', 'Newfoundland and Labrador'),
                          ('NT', 'Northwestern Territories'),
                          ('NS', 'Nova Scotia'),
                          ('NU', 'Nunavut'),
                          ('ON', 'Ontario'),
                          ('PE', 'Prince Edward Island'),
                          ('QC', 'Quebec'),
                          ('SK', 'Saskatchewan'),
                          ('YT', 'Yukon')]
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=2, choices=CANADIAN_PROVINCES)
    country = models.CharField(max_length=20)
    street_address = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        s = self.street_address + ", " + self.city + ', ' + self.province + ', ' + self.country + ', ' \
            + self.postal_code
        return s


class Menu(models.Model):
    title = models.CharField(max_length=150, verbose_name='Menu Title')
    from_time = models.TimeField(verbose_name='Starts at')
    to_time = models.TimeField(verbose_name="Ends at")

    def __str__(self):
        s = ''
        if self.restaurant_set.all().count() > 0:
            s += self.restaurant_set.all()[0].name

        s += ': ' + self.title
        return s


class FoodItem(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=70, blank=True, null=True)
    price = models.FloatField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.menu is not None:
            return str(self.menu.title) + ": " + self.name
        else:
            return str(self.name)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        s = self.first_name + ' ' + self.last_name
        return s


class OrderFoodItem(models.Model):
    quantity = models.IntegerField(default=0)
    food_item = models.ForeignKey(FoodItem, on_delete=models.PROTECT)

    def __str__(self):
        return self.food_item.name + ": " + str(self.quantity)


class Order(models.Model):
    ORDER_STATUS = [('SUB', 'submitted'),
                    ('PRG', "In progress"),
                    ('CMP', "Completed")]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    # food_items = models.ManyToManyField(FoodItem)
    items = models.ManyToManyField(OrderFoodItem)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_and_time = models.DateTimeField(editable=False, auto_now_add=True)
    order_total = models.FloatField(editable=False)
    status = models.CharField(max_length=3, choices=ORDER_STATUS, default='SUB')

    # todo: implement rating field to allow customer to add rating to order

    def __str__(self):
        return "Order number: " + str(self.id)


class RestaurantTaxRate:
    tax_rate = {
        "BC": 5,
        "AB": 5,
        "MB": 12,
        "NB": 15,
        "NL": 15,
        "NS": 15,
        "ON": 13,
        "PE": 15,
        "QC": 14.975,
        "SK": 11,
        "NT": 5,
        "NU": 5,
        "YK": 5
    }
