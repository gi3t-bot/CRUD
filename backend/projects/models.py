"""
Project model.
A project is owned by an admin and can have multiple members (users).
"""

from django.db import models
from django.conf import settings


class Project(models.Model):
    """
    Represents a team project.
    - owner: The admin who created it
    - members: All users (including owner) who have access
    """

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',  # user.owned_projects.all()
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='member_projects',  # user.member_projects.all()
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest first

    def __str__(self):
        return self.name
