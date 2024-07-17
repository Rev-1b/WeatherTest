from django.urls import path

from weather import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

]
