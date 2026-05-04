"""
Views for the tasks app.
Key design decisions:
- Admins can create/assign/delete tasks
- Members can only update status of tasks assigned to them
- Dashboard stats are computed here
"""

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer
from projects.models import Project


class TaskListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/tasks/?project=<id> — list tasks (filtered by project)
    POST /api/tasks/              — create a task (admin only)
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Admins see all tasks in their projects.
        Members only see tasks assigned to them.
        """
        user = self.request.user
        project_id = self.request.query_params.get('project')

        if user.role == 'admin':
            # Admin sees all tasks in projects they own
            qs = Task.objects.filter(project__owner=user)
        else:
            # Member only sees their assigned tasks
            qs = Task.objects.filter(assigned_to=user)

        # Optional project filter
        if project_id:
            qs = qs.filter(project_id=project_id)

        return qs.select_related('project', 'assigned_to', 'created_by')

    def perform_create(self, serializer):
        """Only admins can create tasks."""
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admins can create tasks.")
        serializer.save()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/tasks/<id>/ — view task
    PUT    /api/tasks/<id>/ — update task
    DELETE /api/tasks/<id>/ — delete task (admin only)
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.filter(project__owner=user)
        # Members can only access their own tasks
        return Task.objects.filter(assigned_to=user)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        # Members can only update status — not reassign, delete, etc.
        if request.method in ['PUT', 'PATCH']:
            if request.user.role == 'member':
                allowed_fields = {'status'}
                incoming_fields = set(request.data.keys())
                if not incoming_fields.issubset(allowed_fields):
                    raise PermissionDenied("Members can only update task status.")
        # Only admins can delete
        if request.method == 'DELETE' and request.user.role != 'admin':
            raise PermissionDenied("Only admins can delete tasks.")


class DashboardStatsView(APIView):
    """
    GET /api/tasks/dashboard/
    Returns summary stats for the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        if user.role == 'admin':
            # Admins see stats for all tasks in their projects
            all_tasks = Task.objects.filter(project__owner=user)
        else:
            # Members see stats for tasks assigned to them
            all_tasks = Task.objects.filter(assigned_to=user)

        total = all_tasks.count()
        completed = all_tasks.filter(status='completed').count()
        in_progress = all_tasks.filter(status='in_progress').count()
        pending = all_tasks.filter(status='pending').count()
        overdue = all_tasks.filter(
            due_date__lt=today
        ).exclude(status='completed').count()

        # My tasks (always the logged-in user's assigned tasks)
        my_tasks = Task.objects.filter(assigned_to=user).count()

        return Response({
            'total_tasks': total,
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'overdue': overdue,
            'my_tasks': my_tasks,
        })
