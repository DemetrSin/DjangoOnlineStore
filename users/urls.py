from django.urls import path

from .api_views import ClientListView, OrderListView, OrderItemListView, ReviewListView
from .views import (ClientCreateView, CustomLoginView, CustomLogoutView,
                    CustomUserRegisterView, HomeView, ProfileUpdateView,
                    ProfileView, ClientUpdateView, ReviewCreateView, ReviewsDetailView, AccountDeleteView)

urlpatterns = [
    path('api/v1/clients', ClientListView.as_view()),
    path('api/v1/orders', OrderListView.as_view()),
    path('api/v1/order_items', OrderItemListView.as_view()),
    path('api/v1/reviews', ReviewListView.as_view()),
    path('home', HomeView.as_view(), name='home'),
    path('register', CustomUserRegisterView.as_view(), name='register'),
    path('account_delete', AccountDeleteView.as_view(), name='account_delete'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', CustomLogoutView.as_view(), name='logout'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_profile', ProfileUpdateView.as_view(), name='update_profile'),
    path('client', ClientCreateView.as_view(), name='client'),
    path('client_update', ClientUpdateView.as_view(), name='client_update'),
    path('review_create', ReviewCreateView.as_view(), name='review_create'),
    path('reviews_detail', ReviewsDetailView.as_view(), name='reviews_detail')
]
