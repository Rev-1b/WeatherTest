from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm


class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        super(UserRegisterView, self).form_valid(form)
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    next_page = 'index'
    form_class = AuthenticationForm
