from django.contrib import admin
from .models import PreviousYearPaper

class PreviousYearPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'paper_type', 'year', 'uploaded_by', 'created_at']
    list_filter = ['paper_type', 'year', 'created_at']
    search_fields = ['title', 'course__course_code', 'course__title', 'uploaded_by__username']
    readonly_fields = ['created_at']
    ordering = ['-year', '-created_at']

admin.site.register(PreviousYearPaper, PreviousYearPaperAdmin)
