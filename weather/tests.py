from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .models import CityModel

User = get_user_model()


class IndexViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
        self.default_city = settings.DEFAULT_CITY

        self.user = User.objects.create_user(username='NewUser', password='1234')
        self.city = CityModel.objects.create(name=self.default_city)

    @patch('utils.api_requests.get_city_info')
    @patch('utils.api_requests.get_city_forecast')
    def test_get(self, mock_get_city_forecast, mock_get_city_info):
        setup_mocks(mock_get_city_forecast, mock_get_city_info)
        self.client.login(username='NewUser', password='1234')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/index.html')
        self.assertIn('form', response.context)
        self.assertIn('name', response.context)
        self.assertIn('weather', response.context)
        self.assertIn('forecast', response.context)
        self.assertIn('cities', response.context)  # Проверяем наличие городов для авторизованного пользователя

    @patch('utils.api_requests.get_city_info')
    @patch('utils.api_requests.get_city_forecast')
    def test_post_valid_city(self, mock_get_city_forecast, mock_get_city_info):
        setup_mocks(mock_get_city_forecast, mock_get_city_info)

        response = self.client.post(self.url, {'city_name': self.default_city})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/index.html')
        self.assertIn('form', response.context)
        self.assertIn('name', response.context)
        self.assertIn('weather', response.context)
        self.assertIn('forecast', response.context)

    @patch('utils.api_requests.get_city_info')
    @patch('utils.api_requests.get_city_forecast')
    def test_post_invalid_city(self, mock_get_city_forecast, mock_get_city_info):
        mock_get_city_info.return_value.status_code = 404
        mock_get_city_forecast.return_value.status_code = 404
        message = 'Город "Invalid City" не был найден. Пожалуйста, проверьте введенное значение!'

        response = self.client.post(self.url, {'city_name': 'Invalid City'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/index.html')
        self.assertIn('form', response.context)
        self.assertIn('error_message', response.context)
        self.assertEqual(response.context.get('error_message'), message)

    def test_authenticated_user_history(self):
        self.client.login(username='NewUser', password='1234')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('cities', response.context)

    def test_unauthenticated_user_history(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('cities', response.context)


def setup_mocks(mock_get_city_forecast, mock_get_city_info):
    mock_get_city_info.return_value.json.return_value = {
        'weather': [{'icon': '01d'}],
        'main': {'temp': 25, 'feels_like': 20},
        'sys': {'sunrise': 1625680800, 'sunset': 1625737200},
        'timezone': 10800
    }
    mock_get_city_forecast.return_value.json.return_value = {
        'list': [
            {'dt': 1625680800, 'main': {'temp': 25, 'feels_like': 20}, 'weather': [{'icon': '01d'}]},
            {'dt': 1625767200, 'main': {'temp': 26, 'feels_like': 21}, 'weather': [{'icon': '02d'}]}
        ]
    }


class StatisticViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('statistic')
        self.default_city = settings.DEFAULT_CITY

    def test_get_request_no_city_in_db(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('error_message'), f'Город "{self.default_city}" никогда не был запрошен.')

    def test_get_request_city_in_db(self):
        CityModel.objects.create(name=self.default_city, searched=0)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_request_city_in_db(self):
        CityModel.objects.create(name='Test City', searched=0)
        form_data = {'city_name': 'Test City'}
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test City')

    def test_post_request_city_not_in_db(self):
        form_data = {'city_name': 'Nonexistent City'}
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('error_message'), 'Город "Nonexistent City" никогда не был запрошен.')

    def test_post_request_invalid_form(self):
        form_data = {'city_name': ''}
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Выбранный вами город не прошел валидацию. Пожалуйста, проверьте введенное значение!')
