from django.db import models

from projects.choices import SNIPPET_TYPE_CHOICES


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subproject(models.Model):
    project = models.ForeignKey(
        Project, related_name="subprojects", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.project.name})"


class SubprojectGroup(models.Model):
    subproject = models.ForeignKey(
        Subproject, related_name="subproject_groups", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subproject.name}"


class Snippet(models.Model):
    subproject_group = models.ForeignKey(
        SubprojectGroup, related_name="snippets", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=SNIPPET_TYPE_CHOICES)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.subproject_group.name}"
