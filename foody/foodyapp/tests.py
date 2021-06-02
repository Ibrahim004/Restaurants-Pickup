from django.test import TestCase
from .models import *
from datetime import time


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
