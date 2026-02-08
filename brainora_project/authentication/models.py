from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    """Extended User model for Brainora"""
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    college_id = models.CharField(max_length=50, blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True, choices=[(i, i) for i in range(1, 9)])
    
    def __str__(self):
        return self.username


class Course(models.Model):
    """Course model"""
    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]
    
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    credits = models.IntegerField(default=4)
    instructor = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['semester', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.title}"


class PreviousYearPaper(models.Model):
    """Previous Year Papers model"""
    PAPER_TYPE = [
        ('midterm', 'Midterm Exam'),
        ('final', 'Final Exam'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='papers')
    title = models.CharField(max_length=200)
    paper_type = models.CharField(max_length=20, choices=PAPER_TYPE)
    year = models.IntegerField()
    file = models.FileField(upload_to='papers/')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-created_at']
    
    def __str__(self):
        return f"{self.course.code} - {self.paper_type} ({self.year})"


class CollegeActivity(models.Model):
    """College Activities/Updates model"""
    ACTIVITY_TYPE = [
        ('event', 'Event'),
        ('announcement', 'Announcement'),
        ('holiday', 'Holiday'),
        ('notice', 'Notice'),
        ('deadline', 'Deadline'),
    ]
    
    title = models.CharField(max_length=300)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='activities/', blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return self.title


class Resource(models.Model):
    """Generic resource uploaded by users (notes, assignments, lab files, PYQ, links)"""
    CATEGORY_CHOICES = [
        ('notes', 'Notes'),
        ('assignment', 'Assignment'),
        ('lab', 'Lab File'),
        ('pyq', 'PYQ'),
        ('roadmap', 'Roadmap'),
        ('whatsapp', 'Whatsapp Community'),
        ('official', 'Official Links'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='uploaded_resources')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
