import requests


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