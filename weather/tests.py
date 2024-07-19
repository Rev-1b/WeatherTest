from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserAuthTests(TestCase):

    def setUp(self):
        self.username = 'TestUser'
        self.password = 'TestPassword123'
        User.objects.create_user(username=self.username, password=self.password)

    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'new_user',
            'password1': 'new_password123',
            'password2': 'new_password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='new_user').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после успешного логаута
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.get(reverse('logout'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
