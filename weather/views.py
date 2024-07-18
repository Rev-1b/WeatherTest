from datetime import datetime

import pytz
import requests
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

from weather.forms import CityForm
from weather.models import CityModel


class IndexView(View):
    template_name = 'weather/index.html'

    def get_queryset(self):
        return CityModel.objects.all()

    def get_context_data(self, **kwargs):
        weather = kwargs.get('weather')
        forecast = kwargs.get('forecast')
        form = kwargs.get('form')
        context = {
            'form': form,
            'weather': {
                'weather_icon': weather['weather'][0]['icon'],
                'temp': round(weather['main']['temp']),
                'feels_like': round(weather['main']['feels_like']),
                'time': get_current_time(weather['timezone']),
                'sunrise': convert_unix_to_local(weather['sys']['sunrise'], weather['timezone']),
                'sunset': convert_unix_to_local(weather['sys']['sunset'], weather['timezone']),
                'name': weather['name'], 'is_authenticated': False,
            },
            'forecast': [],
        }

        for elem in forecast['list']:
            result = {
                'time': convert_unix_to_local(elem['dt'], weather['timezone']),
                'temp': elem['main']['temp'],
                'feels_like': elem['main']['feels_like'],
                'weather_icon': elem['weather'][0]['icon'],
            }
            context['forecast'].append(result)

        if self.request.user.is_authenticated:
            context['cities'] = self.get_queryset().filter(
                user=self.request.user).values('name').distinct()[:10]

            context['is_authenticated'] = True

        return context

    def get(self, request):
        city_name = 'Moscow'
        form = CityForm()

        weather = get_city_info(city_name)
        forecast = get_city_forecast(city_name)

        return render(request, self.template_name, self.get_context_data(
            form=form, weather=weather.json(), forecast=forecast.json()
        ))

    def post(self, request, *args, **kwargs):
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']

            weather = get_city_info(city_name)
            forecast = get_city_forecast(city_name)

            if weather.status_code != 200 or forecast.status_code != 200:
                return HttpResponseBadRequest('Неправильный город')

            user = request.user if request.user.is_authenticated else None
            city = self.get_queryset().create(name=city_name)

            if user is not None:
                user.cities.add(city)

            return render(request, self.template_name, self.get_context_data(
                form=form, weather=weather.json(), forecast=forecast.json()
            ))
        return HttpResponseBadRequest('Неправильный город')


def get_current_time(offset_seconds):
    offset_hours = offset_seconds // 3600
    tz = pytz.FixedOffset(offset_hours * 60)
    current_time = datetime.now(tz)
    return current_time.strftime('%H:%M:%S')


def convert_unix_to_local(unix_timestamp, offset_seconds):
    offset_hours = offset_seconds // 3600
    tz = pytz.FixedOffset(offset_hours * 60)

    local_time = datetime.fromtimestamp(unix_timestamp, tz=tz)
    return local_time.strftime('%H:%M:%S')


def get_city_info(city):
    current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
    api_key = '1600667aec76cc2ab680ca18f43b89c0'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
    }
    return requests.get(current_weather_url, params=params)


def get_city_forecast(city):
    current_weather_url = 'http://api.openweathermap.org/data/2.5/forecast'
    api_key = '1600667aec76cc2ab680ca18f43b89c0'
    params = {
        'q': city,
        'appid': api_key,
        'cnt': 3,
        'units': 'metric',
    }
    return requests.get(current_weather_url, params=params)
