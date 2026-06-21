from django.db import models
from django.conf import settings

class Resource(models.Model):
    CATEGORY_CHOICES = (
        ('Notes', 'Notes'),
        ('Assignments', 'Assignments'),
        ('Lab Files', 'Lab Files'),
        ('Previous Year Papers', 'Previous Year Papers'),
        ('Roadmaps', 'Roadmaps'),
        ('WhatsApp Groups', 'WhatsApp Groups'),
        ('Official Resources', 'Official Resources'),
        ('CS3F', 'CS3F'),
        ('Telegram Groups', 'Telegram Groups'),
        ('Holiday Homework', 'Holiday Homework'),
    )

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    external_link = models.URLField(max_length=500, blank=True, null=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_resources')
    
    downloads = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_resources', blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarked_resources', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def total_bookmarks(self):
        return self.bookmarks.count()

    def __str__(self):
        return f"{self.category} - {self.title}"
