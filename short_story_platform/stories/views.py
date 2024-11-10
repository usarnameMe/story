from random import randint

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from .models import CustomUser, Story
from .serializers import CustomUserSerializer, StorySerializer
import redis

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)


# Function-based views
def profile_page(request):
    return render(request, 'profile.html', {'user': request.user})


def story_list_create_page(request):
    stories = Story.objects.filter(is_public=True)
    return render(request, 'story_list.html', {'stories': stories})


def my_stories_page(request):
    stories = Story.objects.filter(author=request.user)
    return render(request, 'my_stories.html', {'stories': stories})


def story_detail_page(request, pk):
    story = get_object_or_404(Story, id=pk, author=request.user)
    return render(request, 'story_detail.html', {'story': story})


# Class-based views
class RegisterUserView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Adjust the URL name as needed

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class GenerateCodeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        code = f"{randint(1000, 9999)}"
        redis_client.setex(f"user_{request.user.id}_code", 3600, code)
        return Response({"code": code}, status=status.HTTP_200_OK)
