from django.db import models
from django.conf import settings

class CollegeActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = (
        ('Event', 'Event'),
        ('Announcement', 'Announcement'),
        ('Notice', 'Notice'),
        ('Holiday', 'Holiday'),
        ('Deadline', 'Deadline'),
    )

    title = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=255, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField()
    activity_date = models.DateField()
    location = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='activities/', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "College Activities"
        ordering = ['-activity_date']

    def __str__(self):
        return f"{self.activity_type} - {self.title}"
