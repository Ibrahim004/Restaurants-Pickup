from django.db import models


# Create your models here.
class Restaurant(models.Model):

    RESTAURANT_TYPE = [('ITL', 'Italian'),
                       ('JPN', 'Japanese'),
                       ('IND', 'Indian'),
                       ('FST', 'Fast Food'),
                       ('SHI', 'Sushi'),
                       ('CHN', 'Chinese')]
    name = models.CharField(max_length=200)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    address = models.CharField(max_length=200)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    genre = models.CharField(max_length=3, choices=RESTAURANT_TYPE, blank=True, null=True)
    menu = models.ManyToManyField('Menu')


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




