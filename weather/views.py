from django.conf import settings
from django.db.models import F
from django.shortcuts import render
from django.views import View

from utils.api_requests import get_city_info, get_city_forecast
from utils.other import get_searched_amount
from utils.time import get_current_time, convert_unix_to_local
from weather.forms import CityForm
from weather.models import CityModel


class IndexView(View):
    template_name = 'weather/index.html'

    def get_queryset(self):
        return CityModel.objects.all()

    @staticmethod
    def prepare_weather_data(weather):
        return {
            'weather_icon': weather['weather'][0]['icon'],
            'temp': round(weather['main']['temp']),
            'feels_like': round(weather['main']['feels_like']),
            'time': get_current_time(weather['timezone']),
            'sunrise': convert_unix_to_local(weather['sys']['sunrise'], weather['timezone']),
            'sunset': convert_unix_to_local(weather['sys']['sunset'], weather['timezone']),
        }

    @staticmethod
    def prepare_forecast_data(forecast, timezone):
        return [
            {
                'time': convert_unix_to_local(elem['dt'], timezone),
                'temp': round(elem['main']['temp']),
                'feels_like': round(elem['main']['feels_like']),
                'weather_icon': elem['weather'][0]['icon'],
            }
            for elem in forecast['list']
        ]

    def get_context_data(self, form, weather=None, forecast=None, city_name=None, error_message=None):
        context = {
            'form': form,
            'name': city_name,
        }

        if error_message:
            context['error_message'] = error_message
        else:
            if weather:
                context['weather'] = self.prepare_weather_data(weather)
            if forecast:
                context['forecast'] = self.prepare_forecast_data(forecast, weather['timezone'])

        if self.request.user.is_authenticated:
            context['cities'] = self.get_queryset().filter(user=self.request.user).order_by('-updated_at')[:20]

        return context

    def get(self, request):
        city_name = settings.DEFAULT_CITY  # The city that will be displayed when you first visit the site
        form = CityForm()

        weather = get_city_info(city_name)
        forecast = get_city_forecast(city_name)

        return render(request, self.template_name, self.get_context_data(
            form=form, weather=weather.json(), forecast=forecast.json(), city_name=city_name
        ))

    def post(self, request, *args, **kwargs):
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']

            weather = get_city_info(city_name)
            forecast = get_city_forecast(city_name)

            if weather.status_code != 200 or forecast.status_code != 200:
                error_message = f'Город "{city_name}" не был найден. Пожалуйста, проверьте введенное значение!'
                return render(request, self.template_name,
                              self.get_context_data(form=form, error_message=error_message))

            user = request.user if request.user.is_authenticated else None
            city, created = self.get_queryset().get_or_create(name=city_name)

            if not created:
                city.searched = F('searched') + 1
                city.save(update_fields=['searched', 'updated_at'])
                city.refresh_from_db()

            if user is not None:
                user.cities.add(city)

            return render(request, self.template_name, self.get_context_data(
                form=form, weather=weather.json(), forecast=forecast.json(), city_name=city_name
            ))

        error_message = f'Выбранный вами город не прошел валидацию. Пожалуйста, проверьте введенное значение!'
        return render(request, self.template_name,
                      self.get_context_data(form=form, error_message=error_message))


class StatisticView(View):
    template_name = 'weather/statistic.html'

    def get_queryset(self):
        return CityModel.objects.all()

    def get_context_data(self, form=None, city_name=None, error_message=None):
        context = {
            'form': form,
            'name': city_name,
            'searched': get_searched_amount(self.get_queryset(), city_name) if error_message is None else None,
            'error_message': error_message
        }
        return context

    def get(self, request):
        city_name = settings.DEFAULT_CITY
        form = CityForm()
        error_message = None

        if not self.get_queryset().filter(name=city_name).exists():
            error_message = f'Город "{city_name}" никогда не был запрошен.'

        return render(request, self.template_name, self.get_context_data(
            form=form, city_name=city_name, error_message=error_message
        ))

    def post(self, request, *args, **kwargs):
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            if not self.get_queryset().filter(name=city_name).exists():
                error_message = f'Город "{city_name}" никогда не был запрошен.'
            else:
                error_message = None

            return render(request, self.template_name, self.get_context_data(
                form=form, city_name=city_name, error_message=error_message
            ))

        error_message = 'Выбранный вами город не прошел валидацию. Пожалуйста, проверьте введенное значение!'
        return render(request, self.template_name, self.get_context_data(
            form=form, error_message=error_message
        ))