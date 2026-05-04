"""
Custom User model.
Extends Django's AbstractUser to add a 'role' field.
We use AbstractUser so we keep all built-in auth features (password hashing, etc.)
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with role-based access.
    Roles:
      - admin: Can create projects, assign tasks, manage members
      - member: Can only view/update tasks assigned to them
    """

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='member',
    )

    # email is required and must be unique
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        """Convenience property to check admin role."""
        return self.role == 'admin'
