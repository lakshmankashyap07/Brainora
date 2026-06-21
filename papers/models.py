from django.db import models
from django.conf import settings
from courses.models import Course

class PreviousYearPaper(models.Model):
    PAPER_TYPE_CHOICES = (
        ('Midterm', 'Midterm'),
        ('Final', 'Final'),
        ('Quiz', 'Quiz'),
        ('Assignment', 'Assignment'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='papers')
    title = models.CharField(max_length=255)
    paper_type = models.CharField(max_length=20, choices=PAPER_TYPE_CHOICES)
    year = models.IntegerField()
    pdf_file = models.FileField(upload_to='papers/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.course_code} - {self.title} ({self.year})"
