from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Story


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content', 'is_public']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email')