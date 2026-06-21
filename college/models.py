from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from authentication.models import CustomUser
import os

User = CustomUser

# ============ ANNOUNCEMENTS ============

class AnnouncementCategory(models.Model):
    """Categories for announcements"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7, default='#007bff')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Announcement(models.Model):
    """Official college announcements"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    image = models.ImageField(upload_to='announcements/%Y/%m/', blank=True, null=True)
    attachment = models.FileField(upload_to='announcements/%Y/%m/', blank=True, null=True)
    
    is_pinned = models.BooleanField(default=False, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published', db_index=True)
    
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-is_pinned', '-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status', '-is_pinned']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title

class AnnouncementLike(models.Model):
    """Track likes on announcements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcement_likes')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'announcement')
    
    def __str__(self):
        return f"{self.user.username} likes {self.announcement.title}"

class AnnouncementComment(models.Model):
    """Comments on announcements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcement_comments')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} commented on {self.announcement.title}"

# ============ EVENTS ============

class Event(models.Model):
    """College events and functions"""
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('technical', 'Technical'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=300)
    
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='organized_events')
    organizer_name = models.CharField(max_length=200, blank=True)
    
    poster = models.ImageField(upload_to='events/%Y/%m/')
    
    seats_available = models.PositiveIntegerField(null=True, blank=True)
    seats_registered = models.PositiveIntegerField(default=0)
    
    registration_link = models.URLField(blank=True)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['-start_date']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()
    
    @property
    def is_ongoing(self):
        return self.start_date <= timezone.now() <= self.end_date
    
    @property
    def is_past(self):
        return timezone.now() > self.end_date
    
    @property
    def seats_left(self):
        if self.seats_available:
            return max(0, self.seats_available - self.seats_registered)
        return None

class EventRegistration(models.Model):
    """User registration for events"""
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    
    registered_at = models.DateTimeField(auto_now_add=True)
    attended_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'event')
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class EventReminder(models.Model):
    """Reminders for upcoming events"""
    REMINDER_CHOICES = [
        ('1h', '1 Hour Before'),
        ('6h', '6 Hours Before'),
        ('1d', '1 Day Before'),
        ('3d', '3 Days Before'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_reminders')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders')
    reminder_time = models.CharField(max_length=10, choices=REMINDER_CHOICES, default='1d')
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'event')
    
    def __str__(self):
        return f"Reminder: {self.event.title} for {self.user.username}"

# ============ CLUBS ============

class Club(models.Model):
    """College clubs and student organizations"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    logo = models.ImageField(upload_to='clubs/%Y/%m/')
    banner = models.ImageField(upload_to='clubs/%Y/%m/', blank=True)
    
    founder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='founded_clubs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    member_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class ClubMembership(models.Model):
    """Club membership tracking"""
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('president', 'President'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='club_memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'club')
    
    def __str__(self):
        return f"{self.user.username} - {self.club.name}"

class ClubEvent(models.Model):
    """Events organized by clubs"""
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='club_events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=300)
    image = models.ImageField(upload_to='club_events/%Y/%m/', blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.club.name} - {self.title}"

class ClubGallery(models.Model):
    """Club photos and media"""
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='club_gallery/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.club.name} - Photo"

class ClubAnnouncement(models.Model):
    """Club-specific announcements"""
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.club.name} - {self.title}"

# ============ WORKSHOPS & SEMINARS ============

class Workshop(models.Model):
    """Workshops and seminars"""
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    
    speaker_name = models.CharField(max_length=200)
    speaker_title = models.CharField(max_length=200)
    speaker_bio = models.TextField(blank=True)
    speaker_photo = models.ImageField(upload_to='speakers/%Y/%m/', blank=True)
    speaker_email = models.EmailField(blank=True)
    
    venue = models.CharField(max_length=300)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    
    max_seats = models.PositiveIntegerField()
    registered_count = models.PositiveIntegerField(default=0)
    
    poster = models.ImageField(upload_to='workshops/%Y/%m/')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title

class WorkshopRegistration(models.Model):
    """Workshop registration"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshop_registrations')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'workshop')
    
    def __str__(self):
        return f"{self.user.username} - {self.workshop.title}"

class WorkshopResource(models.Model):
    """Resources shared in workshops"""
    RESOURCE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('doc', 'Document'),
        ('ppt', 'Presentation'),
        ('video', 'Video'),
        ('link', 'Link'),
    ]
    
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    
    file = models.FileField(upload_to='workshop_resources/%Y/%m/', blank=True)
    url = models.URLField(blank=True)
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.workshop.title} - {self.title}"

class WorkshopCertificate(models.Model):
    """Certificates for workshop attendance"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshop_certificates')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='certificates')
    certificate_code = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'workshop')
    
    def __str__(self):
        return f"Certificate: {self.user.username} - {self.workshop.title}"

class WorkshopFeedback(models.Model):
    """Feedback for workshops"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshop_feedback')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='feedback')
    
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField(blank=True)
    
    content_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    speaker_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    venue_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'workshop')
    
    def __str__(self):
        return f"Feedback: {self.user.username} - {self.workshop.title}"

# ============ LOST & FOUND ============

class LostFoundItem(models.Model):
    """Lost and found items"""
    ITEM_TYPE_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]
    
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('accessories', 'Accessories'),
        ('documents', 'Documents'),
        ('clothing', 'Clothing'),
        ('books', 'Books'),
        ('wallet', 'Wallet/Cards'),
        ('keys', 'Keys'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('expired', 'Expired'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    image = models.ImageField(upload_to='lost_found/%Y/%m/')
    
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lost_found_items')
    
    date_lost_found = models.DateField()
    location = models.CharField(max_length=300)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    contact_info = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_items')
    
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['item_type', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"[{self.get_item_type_display()}] {self.title}"

class LostFoundMatch(models.Model):
    """Matching between lost and found items"""
    lost_item = models.ForeignKey(LostFoundItem, on_delete=models.CASCADE, related_name='found_matches', limit_choices_to={'item_type': 'lost'})
    found_item = models.ForeignKey(LostFoundItem, on_delete=models.CASCADE, related_name='lost_matches', limit_choices_to={'item_type': 'found'})
    
    suggested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('lost_item', 'found_item')
    
    def __str__(self):
        return f"Match: {self.lost_item.title} - {self.found_item.title}"

# ============ COMPLAINTS & SUGGESTIONS ============

class Complaint(models.Model):
    """Complaint and suggestion portal"""
    COMPLAINT_TYPE_CHOICES = [
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
    ]
    
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('facility', 'Facility'),
        ('food', 'Food & Cafeteria'),
        ('discipline', 'Discipline'),
        ('hostel', 'Hostel'),
        ('misc', 'Miscellaneous'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints', null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    
    attachment = models.FileField(upload_to='complaints/%Y/%m/', blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    admin_response = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['priority']),
        ]
    
    def __str__(self):
        return self.title

# ============ FACULTY DIRECTORY ============

class FacultyProfile(models.Model):
    """Faculty directory and profiles"""
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_prof', 'Associate Professor'),
        ('assistant_prof', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('visiting_faculty', 'Visiting Faculty'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES)
    department = models.CharField(max_length=100)
    
    subjects = models.CharField(max_length=500, help_text="Comma-separated list of subjects")
    research_interests = models.TextField(blank=True)
    
    office_location = models.CharField(max_length=200, blank=True)
    cabin_number = models.CharField(max_length=50, blank=True)
    
    office_phone = models.CharField(max_length=20, blank=True)
    office_hours = models.CharField(max_length=200, blank=True, help_text="e.g., Mon-Wed 2-4 PM")
    
    qualifications = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    
    publications = models.TextField(blank=True)
    
    profile_photo = models.ImageField(upload_to='faculty/%Y/%m/', blank=True)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Faculty Profiles"
        ordering = ['user__first_name']
        indexes = [
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        return f"Prof. {self.user.get_full_name()}"

# ============ CAMPUS MAP ============

class CampusLocation(models.Model):
    """Campus buildings and locations"""
    BUILDING_TYPE_CHOICES = [
        ('academic', 'Academic Block'),
        ('library', 'Library'),
        ('hostel', 'Hostel'),
        ('cafeteria', 'Cafeteria'),
        ('sports', 'Sports Complex'),
        ('lab', 'Laboratory'),
        ('auditorium', 'Auditorium'),
        ('medical', 'Medical Room'),
        ('parking', 'Parking'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    building_type = models.CharField(max_length=20, choices=BUILDING_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    address = models.TextField()
    
    image = models.ImageField(upload_to='campus_locations/%Y/%m/', blank=True)
    
    floor_plan = models.FileField(upload_to='campus_locations/floor_plans/', blank=True)
    
    contact_number = models.CharField(max_length=20, blank=True)
    
    opening_hours = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class CampusNearby(models.Model):
    """Nearby facilities for campus locations"""
    location = models.ForeignKey(CampusLocation, on_delete=models.CASCADE, related_name='nearby')
    nearby_location = models.ForeignKey(CampusLocation, on_delete=models.CASCADE, related_name='nearby_to')
    distance_m = models.PositiveIntegerField(help_text="Distance in meters")
    
    class Meta:
        unique_together = ('location', 'nearby_location')
    
    def __str__(self):
        return f"{self.location.name} near {self.nearby_location.name}"
