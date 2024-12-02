from django.db import models

from accounts.models import User
from guardamelo_api import settings
from projects.choices import NOTE_VISIBILITY_CHOICES
from projects.enums.note_visibility import NoteVisibility


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)

    visibility = models.CharField(
        max_length=10,
        choices=NOTE_VISIBILITY_CHOICES,
        default=NoteVisibility.PRIVATE.value
    )

    shared_with = models.ManyToManyField(
        User,
        blank=True,
        related_name='shared_notes',
        help_text="Users who can view this note if visibility is set to 'shared'.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def user_can_view(self, user):
        if self.visibility == 'public':
            return True
        if self.visibility == 'private':
            return self.project.user == user
        if self.visibility == 'shared':
            return self.shared_with.filter(pk=user.pk).exists()
        return False

    def __str__(self):
        return self.title
