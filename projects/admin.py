from django.contrib import admin

from projects.models import Project, Subproject, SubprojectGroup, Snippet


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Subproject)
class SubprojectAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'created_at')
    search_fields = ('name', 'project__name')
    list_filter = ('project',)
    ordering = ('-created_at',)


@admin.register(SubprojectGroup)
class SubprojectGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'subproject', 'description', 'created_at')
    search_fields = ('name', 'subproject__name')
    list_filter = ('subproject',)
    ordering = ('name', '-created_at')


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'value', 'description', 'file_name', 'created_at')
    search_fields = ('title', 'subproject_group__name', 'type')
    list_filter = ('type', 'subproject_group')
    ordering = ('-created_at',)
