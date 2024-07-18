from django import forms


class CityForm(forms.Form):
    city_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'city-input',
            'placeholder': 'Введите название города'
        })
    )