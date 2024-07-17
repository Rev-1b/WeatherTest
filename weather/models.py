from django.contrib.auth.models import User
from django.db import models


class CityModel(models.Model):
    name = models.CharField(max_length=50)
    user = models.ManyToManyField(to=User, related_name='cities', verbose_name="Пользователь")

    def __str__(self):
        return self.name
