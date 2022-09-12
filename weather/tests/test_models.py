from django.test import TestCase
from weather.models import City


class CityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        City.objects.create(title="Test City")

    def test_title_max_length(self):
        city = City.objects.get(id=1)
        max_length = city._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)

    def test_city_str(self):
        city = City.objects.get(id=1)
        self.assertEqual(str(city), city.title)

    def test_title_label(self):
        city = City.objects.get(id=1)
        field_label = city._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'City name')
