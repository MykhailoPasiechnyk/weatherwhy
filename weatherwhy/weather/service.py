from django.conf import settings
import requests
import abc


class Params(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_params(**kwargs) -> dict:
        pass


class WeatherAPIParams(Params):
    @staticmethod
    def get_params(city_name: str, api_key, units) -> dict:
        return {'q': city_name, 'appid': api_key, 'units': units}


class WeatherCity:
    def __init__(self, data):
        self._data = data

    def get_description(self) -> str:
        return self._data['weather'][0]['description']

    def get_icon_id(self) -> str:
        return self._data['weather'][0]['icon']

    def get_temperature(self) -> str:
        return self._data['main']['temp']


class WeatherService:
    API_KEY = settings.WEATHER_API_KEY
    URL = settings.WEATHER_URL
    UNITS = settings.WEATHER_UNITS

    @staticmethod
    def _get_default_context():
        return {
            'city': 'City Name',
            'description': 'Weather description',
            'icon': 'default icon',
            'temp': 'Temperature',
        }

    @staticmethod
    def _get_weather(city_name: str):
        params = WeatherAPIParams.get_params(city_name, WeatherService.API_KEY, WeatherService.UNITS['metric'])
        return requests.get(url=WeatherService.URL, params=params).json()

    @staticmethod
    def get_weather_context(city_name: str) -> dict:
        if city_name == '':
            return WeatherService._get_default_context()

        response = WeatherService._get_weather(city_name)

        if response['cod'] == '404':
            return WeatherService._get_default_context()

        weather_city = WeatherCity(response)
        weather_description = weather_city.get_description()
        weather_icon = weather_city.get_icon_id()
        weather_temp = weather_city.get_temperature()

        weather_context = {
            'city': city_name,
            'description': weather_description,
            'icon': weather_icon,
            'temp': weather_temp,
        }

        return weather_context
