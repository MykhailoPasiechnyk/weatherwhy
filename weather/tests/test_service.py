from django.test import TestCase
from weather.service import WeatherAPIParams, WeatherCity, WeatherService
from unittest.mock import patch, MagicMock
from weather.exceptions import TitleCityException


class WeatherAPIParamsTest(TestCase):
    def test_get_params(self):
        self.assertDictEqual(WeatherAPIParams.get_params('test', 'api_key', 'test'),
                             {'q': 'test', 'appid': 'api_key', 'units': 'test'})


# TODO: cover all get cases
# dont depends on API
class WeatherCityTest(TestCase):
    @classmethod
    def get_weather_city_instance(cls):
        return WeatherCity(
            {'main': {'temp': 23},
             'weather': [{
                 'description': 'test_desc',
                 'icon': 'test_icon_id'}, ]
             })

    def test_get_description(self):
        weather_city = WeatherCityTest.get_weather_city_instance()
        self.assertEqual(weather_city.get_description(), 'test_desc')

    def test_get_icon_id(self):
        weather_city = WeatherCityTest.get_weather_city_instance()
        self.assertEqual(weather_city.get_icon_id(), 'test_icon_id')

    def test_get_temperature(self):
        weather_city = WeatherCityTest.get_weather_city_instance()
        self.assertEqual(weather_city.get_temperature(), 23)


class WeatherServiceTest(TestCase):
    @patch('weather.service.requests')
    def test_get_weather_context_bad_request(self, requests_mock):
        request_response_mock = MagicMock()
        request_response_mock.status_code = 404

        requests_mock.get.return_value = request_response_mock

        with self.assertRaises(TitleCityException):
            WeatherService.get_weather_context('')

    @patch('weather.service.requests')
    def test_get_weather_context(self, requests_mock):
        requests_mock.get.return_value.json.return_value = {'main': {'temp': 23},
                                                            'cod': '200',
                                                            'weather': [{
                                                                'description': 'test_desc',
                                                                'icon': 'test_icon_id'}, ]
                                                            }
        self.assertDictEqual(WeatherService.get_weather_context('TestCity'), {
            'city': 'TestCity',
            'description': 'test_desc',
            'icon': 'test_icon_id',
            'temp': 23,
        })
