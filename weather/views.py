from django.db.models import F
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

from utils.api_requests import get_city_info, get_city_forecast
from utils.other import get_searched_amount
from utils.time import get_current_time, convert_unix_to_local
from weather.forms import CityForm
from weather.models import CityModel

from django.conf import settings


class IndexView(View):
    template_name = 'weather/index.html'

    def get_queryset(self):
        return CityModel.objects.all()

    def get_context_data(self, **kwargs):

        weather = kwargs.get('weather')
        forecast = kwargs.get('forecast')
        form = kwargs.get('form')
        city_name = kwargs.get('name')

        # Put only the necessary information into the context from the server response
        context = {
            'form': form,
            'error_message': kwargs.get('error_message', ''),
            'weather': {
                'weather_icon': weather['weather'][0]['icon'],
                'temp': round(weather['main']['temp']),
                'feels_like': round(weather['main']['feels_like']),
                'time': get_current_time(weather['timezone']),
                'sunrise': convert_unix_to_local(weather['sys']['sunrise'], weather['timezone']),
                'sunset': convert_unix_to_local(weather['sys']['sunset'], weather['timezone']),
                'name': city_name,  # The city name matches what the user entered, not what was in the server response
            },
            'forecast': [],  # Create a list for weather forecast objects in advance
        }

        # Extract the necessary information from each forecast object
        for elem in forecast['list']:
            result = {
                'time': convert_unix_to_local(elem['dt'], weather['timezone']),
                'temp': elem['main']['temp'],
                'feels_like': elem['main']['feels_like'],
                'weather_icon': elem['weather'][0]['icon'],
            }
            context['forecast'].append(result)

        # If the user is not authorized, then there is no one to display the browsing history
        if self.request.user.is_authenticated:
            context['cities'] = self.get_queryset().filter(
                user=self.request.user).order_by('-updated_at')[:20]

        return context

    def get(self, request):
        city_name = settings.DEFAULT_CITY  # The city that will be displayed when you first visit the site
        form = CityForm()

        weather = get_city_info(city_name)
        forecast = get_city_forecast(city_name)

        return render(request, self.template_name, self.get_context_data(
            form=form, weather=weather.json(), forecast=forecast.json(), name=city_name
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
            city, created = self.get_queryset().get_or_create(name=city_name)

            if not created:
                city.searched = F('searched') + 1
                city.save(update_fields=['searched', 'updated_at'])
                city.refresh_from_db()

            if user is not None:
                user.cities.add(city)

            return render(request, self.template_name, self.get_context_data(
                form=form, weather=weather.json(), forecast=forecast.json(), name=city_name
            ))
        return HttpResponseBadRequest('Неправильный город')


class StatisticView(View):
    template_name = 'weather/statistic.html'

    def get_queryset(self):
        return CityModel.objects.all()

    def get_context_data(self, **kwargs):
        form = kwargs.get('form')
        city_name = kwargs.get('name')
        context = {
            'form': form,
            'searched': get_searched_amount(self.get_queryset(), city_name),
            'name': city_name,
        }
        return context

    def get(self, request):
        city_name = settings.DEFAULT_CITY  # The city that will be displayed when you first visit the site
        form = CityForm()
        return render(request, self.template_name, self.get_context_data(
            form=form, name=city_name
        ))

    def post(self, request, *args, **kwargs):
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            return render(request, self.template_name, self.get_context_data(
                form=form, name=city_name
            ))
