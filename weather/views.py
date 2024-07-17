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
        response = kwargs.get('response')
        form = kwargs.get('form')
        context = {
            'weather_icon': response['weather'][0]['icon'],
            'temp': round(response['main']['temp']),
            'feels_like': round(response['main']['feels_like']),
            'time': get_current_time_in_timezone(response['timezone']),
            'sunrise': convert_unix_timestamp_to_local_time(response['sys']['sunrise'], response['timezone']),
            'sunset': convert_unix_timestamp_to_local_time(response['sys']['sunset'], response['timezone']),
            'name': response['name'], 'is_authenticated': False,
            'form': form,
        }

        if self.request.user.is_authenticated:
            context['cities'] = self.get_queryset().filter(user=self.request.user)
            context['is_authenticated'] = True

        return context

    def get(self, request):
        city = 'Moscow'
        form = CityForm()
        response = get_city_info(city)
        return render(request, self.template_name, self.get_context_data(response=response.json(), form=form))

    def post(self, request, *args, **kwargs):
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            response = get_city_info(city_name)

            user = request.user if request.user.is_authenticated else None
            city = self.get_queryset().create(name=city_name)

            if user is not None:
                user.cities.add(city)

            return render(request, self.template_name, self.get_context_data(response=response.json(), form=form))
        return HttpResponseBadRequest('Неправильный город')


def get_current_time_in_timezone(offset_seconds):
    offset_hours = offset_seconds // 3600
    tz = pytz.FixedOffset(offset_hours * 60)
    current_time = datetime.now(tz)
    return current_time.strftime('%H:%M:%S')


def convert_unix_timestamp_to_local_time(unix_timestamp, offset_seconds):
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
    current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
    api_key = '1600667aec76cc2ab680ca18f43b89c0'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
    }
    return requests.get(current_weather_url, params=params)



