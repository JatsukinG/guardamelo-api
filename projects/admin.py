from django.contrib import admin

from projects.models import Project, Document


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_at')
    search_fields = ('title', 'project__name')
    list_filter = ('project',)
    ordering = ('-created_at',)
