from django.contrib import admin
from .models import (
    AcademicResource, AcademicResourceDownload, AcademicResourceBookmark,
    AcademicResourceLike, AcademicResourceReport, Syllabus,
    AcademicCalendar, TimeTable
)

@admin.register(AcademicResource)
class AcademicResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'semester', 'subject', 'status', 'uploaded_by', 'uploaded_at')
    list_filter = ('resource_type', 'semester', 'status', 'is_official', 'uploaded_at')
    search_fields = ('title', 'subject', 'course_code')
    readonly_fields = ('file_size', 'file_type', 'view_count', 'download_count', 'like_count')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'resource_type')
        }),
        ('Academic Details', {
            'fields': ('semester', 'subject', 'department', 'course_code')
        }),
        ('File Information', {
            'fields': ('file', 'file_size', 'file_type')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'uploaded_at', 'updated_at')
        }),
        ('Statistics', {
            'fields': ('view_count', 'download_count', 'like_count')
        }),
        ('Moderation', {
            'fields': ('status', 'approved_by', 'rejection_reason')
        }),
        ('Additional', {
            'fields': ('is_official', 'is_featured')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AcademicResourceDownload)
class AcademicResourceDownloadAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'downloaded_at')
    list_filter = ('downloaded_at',)
    search_fields = ('resource__title', 'user__username')
    readonly_fields = ('downloaded_at',)


@admin.register(AcademicResourceBookmark)
class AcademicResourceBookmarkAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'bookmarked_at')
    list_filter = ('bookmarked_at',)
    search_fields = ('resource__title', 'user__username')


@admin.register(AcademicResourceLike)
class AcademicResourceLikeAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'liked_at')
    list_filter = ('liked_at',)
    search_fields = ('resource__title', 'user__username')


@admin.register(AcademicResourceReport)
class AcademicResourceReportAdmin(admin.ModelAdmin):
    list_display = ('resource', 'reported_by', 'reason', 'is_resolved', 'reported_at')
    list_filter = ('reason', 'is_resolved', 'reported_at')
    search_fields = ('resource__title', 'reported_by__username')


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('semester', 'department', 'created_at')
    list_filter = ('semester', 'department', 'created_at')
    search_fields = ('department',)


@admin.register(AcademicCalendar)
class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'is_important')
    list_filter = ('is_important', 'event_date')
    search_fields = ('title',)
    ordering = ('event_date',)


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('semester', 'department', 'day', 'time_slot', 'subject')
    list_filter = ('semester', 'department', 'day')
    search_fields = ('subject', 'faculty')
