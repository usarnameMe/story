from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import RegisterUserView, GenerateCodeView, profile_page, story_list_create_page, my_stories_page, \
    story_detail_page, update_profile_image
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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
