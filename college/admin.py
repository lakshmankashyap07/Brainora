from django.contrib import admin
from django.utils.html import format_html
from .models import *

# ============ ANNOUNCEMENTS ============

@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_display', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
    def color_display(self, obj):
        return format_html(
            '<div style="background-color: {}; width: 50px; height: 30px; border-radius: 4px;"></div>',
            obj.color,
        )
    color_display.short_description = 'Color'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'is_pinned', 'view_count', 'like_count', 'published_at']
    list_filter = ['status', 'is_pinned', 'category', 'published_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['view_count', 'like_count', 'comment_count', 'published_at', 'updated_at']
    fieldsets = (
        ('Content', {'fields': ('title', 'content', 'category', 'image', 'attachment')}),
        ('Meta', {'fields': ('author', 'status', 'is_pinned')}),
        ('Stats', {'fields': ('view_count', 'like_count', 'comment_count')}),
        ('Timestamps', {'fields': ('published_at', 'updated_at')}),
    )

@admin.register(AnnouncementLike)
class AnnouncementLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'announcement', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'announcement__title']

@admin.register(AnnouncementComment)
class AnnouncementCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'announcement', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'announcement__title', 'content']

# ============ EVENTS ============

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'start_date', 'venue', 'seats_registered', 'view_count']
    list_filter = ['category', 'start_date', 'is_online']
    search_fields = ['title', 'description', 'venue']
    readonly_fields = ['view_count', 'seats_registered', 'created_at', 'updated_at']
    fieldsets = (
        ('Event Details', {'fields': ('title', 'description', 'category', 'poster')}),
        ('Dates & Time', {'fields': ('start_date', 'end_date')}),
        ('Venue', {'fields': ('venue', 'is_online', 'meeting_link')}),
        ('Organizer', {'fields': ('organizer', 'organizer_name')}),
        ('Registration', {'fields': ('seats_available', 'seats_registered', 'registration_link')}),
        ('Stats', {'fields': ('view_count',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'registered_at']
    list_filter = ['status', 'registered_at']
    search_fields = ['user__username', 'event__title']

@admin.register(EventReminder)
class EventReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'reminder_time', 'is_sent']
    list_filter = ['reminder_time', 'is_sent']
    search_fields = ['user__username', 'event__title']

# ============ CLUBS ============

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'founder', 'member_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['member_count', 'created_at', 'updated_at']

@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'club', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['user__username', 'club__name']

@admin.register(ClubEvent)
class ClubEventAdmin(admin.ModelAdmin):
    list_display = ['club', 'title', 'start_date', 'venue']
    list_filter = ['start_date', 'club']
    search_fields = ['title', 'club__name']

@admin.register(ClubGallery)
class ClubGalleryAdmin(admin.ModelAdmin):
    list_display = ['club', 'caption', 'uploaded_by', 'uploaded_at']
    list_filter = ['club', 'uploaded_at']
    search_fields = ['club__name', 'caption']

@admin.register(ClubAnnouncement)
class ClubAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['club', 'title', 'posted_by', 'created_at']
    list_filter = ['club', 'created_at']
    search_fields = ['title', 'club__name']

# ============ WORKSHOPS ============

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker_name', 'start_date', 'status', 'registered_count', 'max_seats']
    list_filter = ['status', 'start_date', 'is_online']
    search_fields = ['title', 'speaker_name']
    readonly_fields = ['registered_count', 'created_at']
    fieldsets = (
        ('Workshop Details', {'fields': ('title', 'description', 'poster', 'status')}),
        ('Dates & Time', {'fields': ('start_date', 'end_date', 'registration_deadline')}),
        ('Speaker', {'fields': ('speaker_name', 'speaker_title', 'speaker_bio', 'speaker_photo', 'speaker_email')}),
        ('Venue', {'fields': ('venue', 'is_online', 'meeting_link')}),
        ('Registration', {'fields': ('max_seats', 'registered_count')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )

@admin.register(WorkshopRegistration)
class WorkshopRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'workshop', 'registered_at']
    search_fields = ['user__username', 'workshop__title']

@admin.register(WorkshopResource)
class WorkshopResourceAdmin(admin.ModelAdmin):
    list_display = ['workshop', 'title', 'resource_type', 'uploaded_at']
    list_filter = ['resource_type', 'uploaded_at']
    search_fields = ['workshop__title', 'title']

@admin.register(WorkshopCertificate)
class WorkshopCertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'workshop', 'certificate_code', 'issued_at']
    search_fields = ['user__username', 'workshop__title', 'certificate_code']
    readonly_fields = ['issued_at']

@admin.register(WorkshopFeedback)
class WorkshopFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'workshop', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'workshop__title']

# ============ LOST & FOUND ============

@admin.register(LostFoundItem)
class LostFoundItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'item_type', 'category', 'status', 'posted_by', 'view_count']
    list_filter = ['item_type', 'category', 'status', 'date_lost_found']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['view_count', 'created_at']

@admin.register(LostFoundMatch)
class LostFoundMatchAdmin(admin.ModelAdmin):
    list_display = ['lost_item', 'found_item', 'suggested_by', 'created_at']
    search_fields = ['lost_item__title', 'found_item__title']

# ============ COMPLAINTS ============

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'complaint_type', 'status', 'priority', 'posted_by', 'assigned_to']
    list_filter = ['status', 'priority', 'category', 'complaint_type', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Details', {'fields': ('title', 'description', 'complaint_type', 'category', 'priority')}),
        ('Author', {'fields': ('posted_by', 'is_anonymous')}),
        ('Management', {'fields': ('status', 'assigned_to', 'admin_response')}),
        ('Attachment', {'fields': ('attachment',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'resolved_at')}),
    )

# ============ FACULTY ============

@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'designation', 'department', 'is_verified', 'experience_years']
    list_filter = ['designation', 'department', 'is_verified']
    search_fields = ['user__first_name', 'user__last_name', 'subjects']
    readonly_fields = ['created_at', 'updated_at']

# ============ CAMPUS MAP ============

@admin.register(CampusLocation)
class CampusLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'building_type', 'latitude', 'longitude']
    list_filter = ['building_type']
    search_fields = ['name', 'address']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CampusNearby)
class CampusNearbyAdmin(admin.ModelAdmin):
    list_display = ['location', 'nearby_location', 'distance_m']
    search_fields = ['location__name', 'nearby_location__name']

