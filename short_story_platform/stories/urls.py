from django.urls import path
from .views import (
    RegisterUserView, GenerateCodeView, profile_page, story_list_create_page,
    my_stories_page, story_detail_page, update_profile_image,
    create_story, delete_story, toggle_story_visibility,
    CreateStoryAPIView, StoryListCreateView,
)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', profile_page, name='profile'),
    path('update-profile-image/', update_profile_image, name='update_profile_image'),
    path('stories/', story_list_create_page, name='story_list_create'),
    path('my-stories/', my_stories_page, name='my_stories'),
    path('stories/<int:pk>/', story_detail_page, name='story_detail'),
    path('generate-code/', GenerateCodeView.as_view(), name='generate_code'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('stories/create/', create_story, name='story_create'),

    # path('stories/edit/<int:pk>/', edit_story, name='story_edit'),
    path('stories/delete/<int:pk>/', delete_story, name='story_delete'),
    path('stories/toggle-visibility/<int:pk>/', toggle_story_visibility, name='story_toggle_visibility'),

    path('stories/api/create/', CreateStoryAPIView.as_view(), name='api_story_create'),
    path('stories/api/list-create/', StoryListCreateView.as_view(), name='api_story_list_create'),
]
