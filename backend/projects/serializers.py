"""Serializers for the projects app."""

from rest_framework import serializers
from .models import Project
from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializes project data.
    owner_detail and members_detail are read-only nested representations
    so the frontend gets full user objects, not just IDs.
    """

    owner_detail = UserSerializer(source='owner', read_only=True)
    members_detail = UserSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description',
            'owner', 'owner_detail',
            'members', 'members_detail',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']

    def create(self, validated_data):
        """Auto-set the owner to the requesting user."""
        members = validated_data.pop('members', [])
        project = Project.objects.create(
            owner=self.context['request'].user,
            **validated_data
        )
        # Add members if provided
        if members:
            project.members.set(members)
        # Always add owner as a member too
        project.members.add(self.context['request'].user)
        return project
