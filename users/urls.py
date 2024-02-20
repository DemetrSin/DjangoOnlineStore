from django.urls import path

from .views import (CustomLoginView, CustomLogoutView, CustomUserRegisterView,
                    HomeView, ProfileUpdateView, ProfileView)

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('register', CustomUserRegisterView.as_view(), name='register'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', CustomLogoutView.as_view(), name='logout'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_profile', ProfileUpdateView.as_view(), name='update_profile')
]
