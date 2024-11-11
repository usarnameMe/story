from django.test import TestCase, Client
from django.urls import reverse

from stories.models import CustomUser


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Logout')

    def test_user_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
