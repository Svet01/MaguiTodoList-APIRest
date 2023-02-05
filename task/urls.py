from django.urls import path
from .views import (
    UserRegisterAPIView, 
    UserProfileAPIView, 
    UserLoginAPIView, 
    UserLogoutAPIView, 
    UserProfileUpdateAPIView, 
    UserDeleteAPIView, 
    UserPasswordUpdateAPIView,
    UserImagenProfileAPIView,
    TaskCreateAPIVIew,
    TaskUserViewAPIView,
    TaskUpdateAPIView,
    TaskDeleteAPIView,
    TagCreateAPIView,
    TagUserViewAPIView,)

urlpatterns = [
    # User EndPoints
    path('user-register/', UserRegisterAPIView.as_view(), name="Register"),
    path('user-login/', UserLoginAPIView.as_view(), name='Login'),
    path('user-logout/', UserLogoutAPIView.as_view(), name='Logout'),
    path('user-update/', UserProfileUpdateAPIView.as_view(), name='UpdateProfile'),
    path('user-password-change/', UserPasswordUpdateAPIView.as_view(), name='UpdatePassword'),
    path('user-imagen-profile-change/', UserImagenProfileAPIView.as_view(), name='UpdateImagenProfile'),
    path('user-profile/', UserProfileAPIView.as_view(), name='Profile'),
    path('user-delete/', UserDeleteAPIView.as_view(), name='Delete'),
    # Task EndPoints
    path('task-create/', TaskCreateAPIVIew.as_view(), name='CreateTask'),
    path('task-view/', TaskUserViewAPIView.as_view(), name='TaskView'),
    path('task-update/<int:task_id>/', TaskUpdateAPIView.as_view(), name='TaskUpdate'),
    path('task-delete/<int:task_id>/', TaskDeleteAPIView.as_view(), name='TaskDelete'),
    # Tags EndPoints
    path('tag-create/', TagCreateAPIView.as_view(), name='TagCreate'),
    path('tag-view/', TagUserViewAPIView.as_view(), name='TagView')
]
