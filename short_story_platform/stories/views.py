from random import randint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from .forms import ProfileImageForm, StoryForm
from .models import CustomUser, Story
from .serializers import CustomUserSerializer, StorySerializer
import redis

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)


class RegisterUserView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


# Regular view for the profile page
@login_required
def profile_page(request):
    return render(request, 'profile.html', {'user': request.user})


# Regular view for listing public stories
def story_list_create_page(request):
    stories = Story.objects.filter(is_public=True)
    return render(request, 'story_list.html', {'stories': stories})


# Regular view for listing the user's own stories
@login_required
def my_stories_page(request):
    stories = Story.objects.filter(author=request.user)
    return render(request, 'my_stories.html', {'stories': stories})


# Regular view for story details
@login_required
def story_detail_page(request, pk):
    story = get_object_or_404(Story, id=pk, author=request.user)
    return render(request, 'story_detail.html', {'story': story})


# Regular view for updating profile image
@login_required
def update_profile_image(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileImageForm(instance=request.user)
    return render(request, 'update_profile_image.html', {'form': form})


# APIView for creating stories
class CreateStoryAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Generic view for listing and creating stories
class StoryListCreateView(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Regular view for deleting a story
@login_required
def delete_story(request, pk):
    story = get_object_or_404(Story, pk=pk, author=request.user)
    if request.method == 'POST':
        story.delete()
        return redirect('my_stories')


# Regular view for toggling story visibility
@login_required
def toggle_story_visibility(request, pk):
    story = get_object_or_404(Story, pk=pk, author=request.user)
    story.is_public = not story.is_public
    story.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'is_public': story.is_public})

    return redirect('my_stories')


@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('my_stories')
    else:
        form = StoryForm()
    return render(request, 'create_story.html', {'form': form})


@login_required
def edit_story(request, pk):
    story_instance = get_object_or_404(Story, pk=pk)
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story_instance)
        if form.is_valid():
            form.save()
            return redirect('my_stories')  # Replace with the correct redirect URL
    else:
        form = StoryForm(instance=story_instance)

    return render(request, 'edit_story.html', {'form': form})


@login_required
def delete_story(request, pk):
    story = get_object_or_404(Story, pk=pk, author=request.user)
    if request.method == 'POST':
        story.delete()
        return redirect('my_stories')
    return render(request, 'delete_story.html', {'story': story})


# View for generating a verification code
class GenerateCodeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        code = f"{randint(1000, 9999)}"
        redis_client.setex(f"user_{request.user.id}_code", 3600, code)
        return Response({"code": code}, status=status.HTTP_200_OK)
