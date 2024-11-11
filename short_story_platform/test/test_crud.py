from django.test import TestCase
from django.urls import reverse

from stories.models import CustomUser, Story


# from .models import Story, CustomUser

class StoryCRUDTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_create_story(self):
        response = self.client.post(reverse('create_story'), {
            'title': 'Test Story',
            'content': 'This is a test story content.',
            'is_public': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Story.objects.filter(title='Test Story').exists())

    def test_read_story(self):
        story = Story.objects.create(
            title='Read Test',
            content='Content for read test',
            is_public=True,
            author=self.user
        )
        response = self.client.get(reverse('story_detail_page', args=[story.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Read Test')

    def test_update_story(self):
        story = Story.objects.create(
            title='Update Test',
            content='Content for update test',
            is_public=True,
            author=self.user
        )
        response = self.client.post(reverse('edit_story', args=[story.id]), {
            'title': 'Updated Title',
            'content': 'Updated content',
            'is_public': True
        })
        self.assertEqual(response.status_code, 302)
        story.refresh_from_db()
        self.assertEqual(story.title, 'Updated Title')

    def test_delete_story(self):
        story = Story.objects.create(
            title='Delete Test',
            content='Content for delete test',
            is_public=True,
            author=self.user
        )
        response = self.client.post(reverse('delete_story', args=[story.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Story.objects.filter(title='Delete Test').exists())
