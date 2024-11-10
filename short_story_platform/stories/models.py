from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)


class Story(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
