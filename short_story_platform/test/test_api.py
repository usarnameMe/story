from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from stories.models import CustomUser


class APIEndpointTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='apiuser', password='password123')
        self.client.login(username='apiuser', password='password123')

    def test_get_stories_api(self):
        response = self.client.get(reverse('api_story_list_create'))  # Updated name
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_story_api(self):
        response = self.client.post(reverse('api_story_list_create'), {  # Updated name
            'title': 'API Story',
            'content': 'API story content',
            'is_public': True
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
