"""URL patterns for the users app."""

from django.urls import path
from .views import RegisterView, ProfileView, UserListView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),          # GET /api/users/
    path('register/', RegisterView.as_view(), name='register'),  # POST /api/users/register/
    path('me/', ProfileView.as_view(), name='profile'),          # GET /api/users/me/
]
