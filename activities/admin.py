from django.contrib import admin
from .models import CollegeActivity

class CollegeActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'activity_date', 'location', 'created_by', 'created_at']
    list_filter = ['activity_type', 'activity_date', 'created_at']
    search_fields = ['title', 'description', 'location', 'created_by__username']
    readonly_fields = ['created_at']
    ordering = ['-activity_date']

admin.site.register(CollegeActivity, CollegeActivityAdmin)
