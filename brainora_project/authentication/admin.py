from django.contrib import admin
from .models import CustomUser, Course, PreviousYearPaper, CollegeActivity


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'college_id', 'semester', 'is_staff')
    search_fields = ('username', 'email', 'college_id')
    list_filter = ('semester', 'is_staff', 'is_superuser')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'semester', 'instructor', 'credits')
    search_fields = ('code', 'title', 'instructor')
    list_filter = ('semester', 'credits')
    ordering = ('semester', 'code')


@admin.register(PreviousYearPaper)
class PreviousYearPaperAdmin(admin.ModelAdmin):
    list_display = ('course', 'paper_type', 'year', 'uploaded_by', 'created_at')
    search_fields = ('course__code', 'course__title', 'title')
    list_filter = ('paper_type', 'year', 'course')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CollegeActivity)
class CollegeActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'date', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('activity_type', 'date', 'created_at')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
