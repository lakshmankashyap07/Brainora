from django import forms
from django.forms import ModelForm
from .models import *

# ============ ANNOUNCEMENTS ============

class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'category', 'image', 'attachment', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Content'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

# ============ EVENTS ============

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'start_date', 'end_date', 'venue', 'poster', 'seats_available', 'registration_link', 'is_online', 'meeting_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
            'seats_available': forms.NumberInput(attrs={'class': 'form-control'}),
            'registration_link': forms.URLInput(attrs={'class': 'form-control'}),
            'is_online': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
        }

class EventRegistrationForm(forms.Form):
    confirm = forms.BooleanField(required=True, label='I confirm my registration for this event')

# ============ CLUBS ============

class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description', 'logo', 'banner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ClubEventForm(ModelForm):
    class Meta:
        model = ClubEvent
        fields = ['title', 'description', 'start_date', 'end_date', 'venue', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

# ============ WORKSHOPS ============

class WorkshopForm(ModelForm):
    class Meta:
        model = Workshop
        fields = ['title', 'description', 'start_date', 'end_date', 'registration_deadline', 'speaker_name', 'speaker_title', 'speaker_bio', 'speaker_photo', 'venue', 'is_online', 'meeting_link', 'max_seats', 'poster']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'speaker_name': forms.TextInput(attrs={'class': 'form-control'}),
            'speaker_title': forms.TextInput(attrs={'class': 'form-control'}),
            'speaker_bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'speaker_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'is_online': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
            'max_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
        }

class WorkshopFeedbackForm(ModelForm):
    class Meta:
        model = WorkshopFeedback
        fields = ['rating', 'content_quality', 'speaker_quality', 'venue_quality', 'comments']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'content_quality': forms.RadioSelect(),
            'speaker_quality': forms.RadioSelect(),
            'venue_quality': forms.RadioSelect(),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# ============ LOST & FOUND ============

class LostFoundItemForm(ModelForm):
    class Meta:
        model = LostFoundItem
        fields = ['title', 'description', 'item_type', 'category', 'image', 'date_lost_found', 'location', 'contact_info']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the item'}),
            'item_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'date_lost_found': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where was it lost/found?'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone or Email'}),
        }

# ============ COMPLAINTS ============

class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'complaint_type', 'category', 'priority', 'is_anonymous', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Complaint Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your complaint'}),
            'complaint_type': forms.RadioSelect(),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ComplaintResponseForm(forms.Form):
    response = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your response...'
        }),
        label='Response'
    )
    status = forms.ChoiceField(
        choices=Complaint.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Update Status'
    )
