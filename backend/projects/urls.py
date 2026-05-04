"""URL patterns for the projects app."""

from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView

urlpatterns = [
    path('', ProjectListCreateView.as_view(), name='project-list'),       # GET, POST
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'), # GET, PUT, DELETE
]
