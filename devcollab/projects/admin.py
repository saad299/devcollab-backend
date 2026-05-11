from django.contrib import admin
from .models import Project, CollaborationRequest

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'status', 'is_open', 'created_at']
    list_filter = ['status', 'is_open']
    search_fields = ['title', 'description', 'tech_stack', 'roles_needed']
    ordering = ['-created_at']

@admin.register(CollaborationRequest)
class CollaborationRequestAdmin(admin.ModelAdmin):
    list_display = ['project', 'requester', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['project__title', 'requester__username']
    ordering = ['-created_at']
