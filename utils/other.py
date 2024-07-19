from django.shortcuts import get_object_or_404


def get_searched_amount(queryset, city_name):
    number = get_object_or_404(queryset, name=city_name).searched
    ending = 'разa' if 2 <= number % 10 <= 4 and not 11 <= number % 100 <= 20 else 'раз'
    return f'{number} {ending}'
