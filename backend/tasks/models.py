"""
Task model.
A task belongs to a project and can be assigned to a member.
"""

from django.db import models
from django.conf import settings
from projects.models import Project


class Task(models.Model):
    """
    Represents a unit of work within a project.
    Status flows: pending → in_progress → completed
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',  # project.tasks.all()
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Task stays if user is deleted
        null=True,
        blank=True,
        related_name='assigned_tasks',  # user.assigned_tasks.all()
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', '-created_at']  # Urgent tasks first

    def __str__(self):
        return f"{self.title} [{self.status}]"
