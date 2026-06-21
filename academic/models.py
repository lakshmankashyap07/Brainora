from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from authentication.models import CustomUser
import os

class AcademicResource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('pyq', 'Previous Year Question Paper'),
        ('notes', 'Notes'),
        ('ebook', 'E-book'),
        ('assignment', 'Assignment'),
        ('lab_manual', 'Lab Manual'),
        ('practical_file', 'Practical File'),
        ('important_questions', 'Important Questions'),
        ('question_bank', 'Question Bank'),
        ('sample_paper', 'Sample Paper'),
        ('faculty_notes', 'Faculty Notes'),
    ]
    
    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    
    # Academic Details
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    subject = models.CharField(max_length=255)
    department = models.CharField(max_length=100, blank=True)
    course_code = models.CharField(max_length=20, blank=True)
    
    # File Information
    file = models.FileField(upload_to='academic_resources/%Y/%m/%d/')
    file_size = models.BigIntegerField(editable=False)  # Size in bytes
    file_type = models.CharField(max_length=10, editable=False)  # pdf, ppt, doc, etc.
    
    # Metadata
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='academic_resources')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Statistics
    download_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    
    # Moderation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_academic_resources')
    rejection_reason = models.TextField(blank=True)
    
    # Additional Fields
    is_official = models.BooleanField(default=False)  # Uploaded by faculty/official
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['-uploaded_at']),
            models.Index(fields=['resource_type', 'semester']),
            models.Index(fields=['subject']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.file_type = os.path.splitext(self.file.name)[1].lower().strip('.')
        super().save(*args, **kwargs)


class AcademicResourceDownload(models.Model):
    """Track downloads for statistics and user history"""
    resource = models.ForeignKey(AcademicResource, on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='downloaded_resources')
    downloaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-downloaded_at']
        unique_together = ['resource', 'user', 'downloaded_at']


class AcademicResourceBookmark(models.Model):
    """Bookmark/Save resources for later"""
    resource = models.ForeignKey(AcademicResource, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookmarked_academic_resources')
    bookmarked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['resource', 'user']
        ordering = ['-bookmarked_at']


class AcademicResourceLike(models.Model):
    """Like system for resources"""
    resource = models.ForeignKey(AcademicResource, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_academic_resources')
    liked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['resource', 'user']


class AcademicResourceReport(models.Model):
    """Report inappropriate resources"""
    REASON_CHOICES = [
        ('inappropriate', 'Inappropriate Content'),
        ('copyright', 'Copyright Violation'),
        ('malware', 'Suspicious File/Malware'),
        ('duplicate', 'Duplicate Resource'),
        ('incomplete', 'Incomplete/Corrupted File'),
        ('other', 'Other'),
    ]
    
    resource = models.ForeignKey(AcademicResource, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='academic_reports')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-reported_at']


class Syllabus(models.Model):
    """Semester-wise syllabus"""
    semester = models.IntegerField(choices=[(i, f'Semester {i}') for i in range(1, 9)])
    department = models.CharField(max_length=100)
    document = models.FileField(upload_to='syllabus/%Y/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ['semester', 'department']
        ordering = ['-semester']
    
    def __str__(self):
        return f"Semester {self.semester} - {self.department}"


class AcademicCalendar(models.Model):
    """Academic calendar and important dates"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_date = models.DateTimeField()
    event_end_date = models.DateTimeField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['event_date']
        verbose_name_plural = "Academic Calendars"
    
    def __str__(self):
        return f"{self.title} - {self.event_date.date()}"


class TimeTable(models.Model):
    """Class timetable"""
    semester = models.IntegerField(choices=[(i, f'Semester {i}') for i in range(1, 9)])
    department = models.CharField(max_length=100)
    day = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ])
    time_slot = models.CharField(max_length=20)  # e.g., "9:00 AM - 10:30 AM"
    subject = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)
    classroom = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['semester', 'department', 'day', 'time_slot']
        ordering = ['semester', 'day', 'time_slot']
    
    def __str__(self):
        return f"{self.semester} - {self.day} {self.time_slot}"
