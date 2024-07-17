# Generated by Django 5.0.7 on 2024-07-17 12:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_alter_citymodel_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citymodel',
            name='user',
        ),
        migrations.AddField(
            model_name='citymodel',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, related_name='cities', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
