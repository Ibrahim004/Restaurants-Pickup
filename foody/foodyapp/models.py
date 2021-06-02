from django.db import models


# Create your models here.
class Restaurant(models.Model):
    RESTAURANT_TYPE = [('ITL', 'Italian'),
                       ('JPN', 'Japanese'),
                       ('IND', 'Indian'),
                       ('FST', 'Fast Food'),
                       ('SHI', 'Sushi'),
                       ('CHN', 'Chinese'),
                       ('BRK', 'Breakfast')]
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
    streetAddress = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        s = self.streetAddress + ", " + self.city + ', ' + self.province + ', ' + self.country + ', ' + self.postal_code
        return s


class Menu(models.Model):
    title = models.CharField(max_length=150)
    from_time = models.TimeField()
    to_time = models.TimeField()

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
        s = self.name
        if self.description:
            s += ': ' + self.description
        return s


class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=16)

    def __str__(self):
        s = self.first_name + ' ' + self.last_name
        return s


class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    food_items = models.ManyToManyField(FoodItem)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_and_time = models.DateTimeField(editable=False, auto_now_add=True)
    order_total = models.FloatField(editable=False)

    def __str__(self):
        return "Order number: " + str(self.id)
