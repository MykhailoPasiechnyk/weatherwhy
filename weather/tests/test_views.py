from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse
from django.contrib.auth.models import User

from weather.models import City

from unittest.mock import patch
from weather.service import WeatherService


class IndexTest(TestCase):
    def test_index_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_index_url_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_index_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'weather/index.html')


class AddCityTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='test', password='12345')
        test_user.save()

    def test_status_code_302(self):
        resp = self.client.get(reverse('add_city'))
        self.assertEqual(resp.status_code, 302)

    def test_redirect_to_home(self):
        resp = self.client.get(reverse('add_city'))
        self.assertRedirects(resp, reverse('home'), status_code=302)

    # TODO: change get weather_context
    @patch('weather.service.WeatherService.get_weather_context', lambda x: {
        'city': 'City Name',
        'description': 'Weather description',
        'icon': 'default icon',
        'temp': 'Temperature',
    })
    def test_if_city_title_in_post(self):
        self.client.login(username='test', password='12345')
        resp = self.client.post(reverse('add_city'), data={'city_title': 'Krakow'})
        self.assertEqual(City.objects.all().count(), 1)
        self.assertRedirects(resp, reverse('home'), status_code=302)

    def test_if_city_title_not_in_post(self):
        resp = self.client.post(reverse('add_city'))
        self.assertEqual(City.objects.all().count(), 0)
        self.assertRedirects(resp, reverse('home'), status_code=302)


class RemoveCityTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='test', password='12345')
        test_user.save()
        City.objects.create(title='Test')

    def test_status_code_302(self):
        resp = self.client.get(reverse('remove_city'))
        self.assertEqual(resp.status_code, 302)

    @patch('weather.service.WeatherService.get_weather_context', lambda x: {
        'city': 'City Name',
        'description': 'Weather description',
        'icon': 'default icon',
        'temp': 'Temperature',
    })
    def test_redirect_to_home(self):
        resp = self.client.get(reverse('remove_city'))
        self.assertRedirects(resp, reverse('home'), status_code=302)

    def test_if_city_remove_in_post(self):
        self.client.login(username='test', password='12345')
        resp = self.client.post(reverse('remove_city'), data={'city_remove': 'Test'})
        self.assertEqual(City.objects.all().count(), 0)
        self.assertRedirects(resp, reverse('home'), status_code=302)

    def test_if_not_city_remove_in_post(self):
        self.client.login(username='test', password='12345')
        resp = self.client.post(reverse('remove_city'))
        self.assertEqual(City.objects.all().count(), 1)
        self.assertRedirects(resp, reverse('home'), status_code=302)


class RegisterTest(TestCase):

    def test_register_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

    def test_register_url_at_desired_location(self):
        resp = self.client.get('/register/')
        self.assertEqual(resp.status_code, 200)

    def test_register_uses_correct_template(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'weather/register.html')

    def test_register_if_request_post_success(self):
        resp = self.client.post(reverse('register'),
                                data={
                                    'username': 'test',
                                    'password1': 'QwehkdfwHjasd123456',
                                    'password2': 'QwehkdfwHjasd123456',
                                    'email': 'some@gmail.com'})
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), 'You have successfully registered')
        self.assertEqual(User.objects.all().count(), 1)
        self.assertRedirects(resp, reverse('login'), status_code=302)

    def test_register_invalid_form(self):
        resp = self.client.post(reverse('register'),
                                data={
                                    'username': 'test',
                                    'password1': 'qwerty',
                                    'password2': 'qwerty',
                                    'email': 'some@gmail.com'})
        messages = list(get_messages(resp.wsgi_request))
        self.assertEqual(str(messages[0]), 'Registration error')
        self.assertEqual(User.objects.all().count(), 0)
        self.assertTemplateUsed(resp, 'weather/register.html')


class UserLoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='test', password='12345')
        test_user.save()

    def test_login_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_login_url_at_desired_location(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    def test_login_uses_correct_template(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'weather/login.html')

    def test_login_valid_form_in_post(self):
        resp = self.client.post(reverse('login'), data={
            'username': 'test',
            'password': '12345'
        })
        self.assertRedirects(resp, reverse('home'), status_code=302)

    def test_login_invalid_form_in_post(self):
        resp = self.client.post(reverse('login'), data={
            'username': 'test',
            'password': '12'
        })
        self.assertTemplateUsed(resp, 'weather/login.html')


class UserLogout(TestCase):
    def test_logout_url_at_desired_location(self):
        resp = self.client.get('/logout/')
        self.assertEqual(resp.status_code, 302)

    def test_status_code_302(self):
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 302)

    def test_redirect_to_login(self):
        resp = self.client.get(reverse('logout'))
        self.assertRedirects(resp, reverse('login'), status_code=302)
