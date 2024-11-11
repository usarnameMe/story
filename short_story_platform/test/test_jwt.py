from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

from stories.models import CustomUser


class JWTAuthorizationTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='jwtuser', password='password123')
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_access_protected_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(reverse('protected_view'))
        self.assertEqual(response.status_code, 200)
