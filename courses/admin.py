from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'title', 'semester', 'credits', 'instructor', 'created_at']
    list_filter = ['semester', 'credits', 'created_at']
    search_fields = ['course_code', 'title', 'instructor']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['course_code']

admin.site.register(Course, CourseAdmin)
