from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),

]
