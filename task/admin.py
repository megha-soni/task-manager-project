from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'status', 'is_completed', 'created_at']
    list_filter = ['status', 'is_completed', 'created_at']
    search_fields = ['title', 'description', 'user__username']