from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from .models import *
from .forms import *

# ============ ANNOUNCEMENTS ============

def announcement_list(request):
    """List all announcements"""
    announcements = Announcement.objects.filter(status='published').prefetch_related('likes', 'comments')
    category = request.GET.get('category')
    search = request.GET.get('q')
    
    if category:
        announcements = announcements.filter(category__slug=category)
    if search:
        announcements = announcements.filter(Q(title__icontains=search) | Q(content__icontains=search))
    
    paginator = Paginator(announcements, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    categories = AnnouncementCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search,
    }
    return render(request, 'college/announcement_list.html', context)

@login_required
def announcement_detail(request, pk):
    """View announcement detail"""
    announcement = get_object_or_404(Announcement, pk=pk, status='published')
    announcement.view_count += 1
    announcement.save()
    
    comments = announcement.comments.all().select_related('user')
    liked = announcement.likes.filter(user=request.user).exists()
    
    context = {
        'announcement': announcement,
        'comments': comments,
        'liked': liked,
    }
    return render(request, 'college/announcement_detail.html', context)

@login_required
def announcement_like(request, pk):
    """Like/Unlike announcement"""
    announcement = get_object_or_404(Announcement, pk=pk)
    like, created = AnnouncementLike.objects.get_or_create(user=request.user, announcement=announcement)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        announcement.like_count = announcement.likes.count()
        announcement.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'like_count': announcement.likes.count()})
    
    return redirect('college:announcement_detail', pk=pk)

@login_required
def announcement_comment(request, pk):
    """Add comment to announcement"""
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = AnnouncementComment.objects.create(
                user=request.user,
                announcement=announcement,
                content=content
            )
            announcement.comment_count = announcement.comments.count()
            announcement.save()
            messages.success(request, 'Comment added!')
    
    return redirect('college:announcement_detail', pk=pk)

# ============ EVENTS ============

def event_list(request):
    """List all events with filtering"""
    events = Event.objects.all().select_related('organizer')
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        events = events.filter(category=category)
    
    # Filter by date range
    date_filter = request.GET.get('date')
    now = timezone.now()
    if date_filter == 'upcoming':
        events = events.filter(start_date__gt=now)
    elif date_filter == 'past':
        events = events.filter(start_date__lt=now)
    
    # Search
    search = request.GET.get('q')
    if search:
        events = events.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
    # Sort
    sort = request.GET.get('sort', '-start_date')
    events = events.order_by(sort)
    
    paginator = Paginator(events, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    categories = Event.CATEGORY_CHOICES
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search,
    }
    return render(request, 'college/event_list.html', context)

@login_required
def event_detail(request, pk):
    """View event details"""
    event = get_object_or_404(Event, pk=pk)
    event.view_count += 1
    event.save()
    
    registered = EventRegistration.objects.filter(user=request.user, event=event).exists()
    
    context = {
        'event': event,
        'registered': registered,
    }
    return render(request, 'college/event_detail.html', context)

@login_required
def event_register(request, pk):
    """Register for an event"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        if event.seats_available and event.seats_registered >= event.seats_available:
            messages.error(request, 'Event is full!')
            return redirect('college:event_detail', pk=pk)
        
        registration, created = EventRegistration.objects.get_or_create(user=request.user, event=event)
        
        if created:
            event.seats_registered += 1
            event.save()
            messages.success(request, 'You have registered for the event!')
        else:
            messages.info(request, 'You are already registered!')
    
    return redirect('college:event_detail', pk=pk)

@login_required
def event_unregister(request, pk):
    """Unregister from an event"""
    event = get_object_or_404(Event, pk=pk)
    registration = EventRegistration.objects.filter(user=request.user, event=event)
    
    if registration.exists():
        registration.delete()
        event.seats_registered = max(0, event.seats_registered - 1)
        event.save()
        messages.success(request, 'Registration cancelled!')
    
    return redirect('college:event_detail', pk=pk)

# ============ CLUBS ============

def club_list(request):
    """List all clubs"""
    clubs = Club.objects.filter(is_active=True).annotate(member_count=Count('members'))
    
    search = request.GET.get('q')
    if search:
        clubs = clubs.filter(Q(name__icontains=search) | Q(description__icontains=search))
    
    paginator = Paginator(clubs, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    context = {
        'page_obj': page_obj,
        'search_query': search,
    }
    return render(request, 'college/club_list.html', context)

@login_required
def club_detail(request, slug):
    """View club details"""
    club = get_object_or_404(Club, slug=slug, is_active=True)
    members = club.members.select_related('user')
    events = club.club_events.all().order_by('-start_date')[:5]
    gallery = club.gallery.all()[:8]
    announcements = club.announcements.all()[:5]
    
    is_member = club.members.filter(user=request.user).exists()
    
    context = {
        'club': club,
        'members': members,
        'events': events,
        'gallery': gallery,
        'announcements': announcements,
        'is_member': is_member,
    }
    return render(request, 'college/club_detail.html', context)

@login_required
def club_join(request, slug):
    """Join a club"""
    club = get_object_or_404(Club, slug=slug)
    
    membership, created = ClubMembership.objects.get_or_create(user=request.user, club=club)
    
    if created:
        club.member_count += 1
        club.save()
        messages.success(request, f'You joined {club.name}!')
    else:
        messages.info(request, 'You are already a member!')
    
    return redirect('college:club_detail', slug=slug)

@login_required
def club_leave(request, slug):
    """Leave a club"""
    club = get_object_or_404(Club, slug=slug)
    membership = ClubMembership.objects.filter(user=request.user, club=club)
    
    if membership.exists():
        membership.delete()
        club.member_count = max(0, club.member_count - 1)
        club.save()
        messages.success(request, f'You left {club.name}!')
    
    return redirect('college:club_list')

# ============ WORKSHOPS ============

def workshop_list(request):
    """List all workshops"""
    workshops = Workshop.objects.all()
    
    status = request.GET.get('status')
    if status:
        workshops = workshops.filter(status=status)
    else:
        workshops = workshops.filter(status__in=['upcoming', 'ongoing'])
    
    search = request.GET.get('q')
    if search:
        workshops = workshops.filter(Q(title__icontains=search) | Q(speaker_name__icontains=search))
    
    workshops = workshops.order_by('-start_date')
    
    paginator = Paginator(workshops, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    context = {
        'page_obj': page_obj,
        'search_query': search,
    }
    return render(request, 'college/workshop_list.html', context)

@login_required
def workshop_detail(request, pk):
    """View workshop details"""
    workshop = get_object_or_404(Workshop, pk=pk)
    registered = WorkshopRegistration.objects.filter(user=request.user, workshop=workshop).exists()
    resources = workshop.resources.all()
    
    context = {
        'workshop': workshop,
        'registered': registered,
        'resources': resources,
    }
    return render(request, 'college/workshop_detail.html', context)

@login_required
def workshop_register(request, pk):
    """Register for a workshop"""
    workshop = get_object_or_404(Workshop, pk=pk)
    
    if workshop.registered_count >= workshop.max_seats:
        messages.error(request, 'Workshop is full!')
        return redirect('college:workshop_detail', pk=pk)
    
    registration, created = WorkshopRegistration.objects.get_or_create(user=request.user, workshop=workshop)
    
    if created:
        workshop.registered_count += 1
        workshop.save()
        messages.success(request, 'You have registered!')
    else:
        messages.info(request, 'You are already registered!')
    
    return redirect('college:workshop_detail', pk=pk)

@login_required
def workshop_feedback(request, pk):
    """Submit workshop feedback"""
    workshop = get_object_or_404(Workshop, pk=pk)
    
    if request.method == 'POST':
        form = WorkshopFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.workshop = workshop
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('college:workshop_detail', pk=pk)
    else:
        form = WorkshopFeedbackForm()
    
    context = {'workshop': workshop, 'form': form}
    return render(request, 'college/workshop_feedback.html', context)

# ============ LOST & FOUND ============

def lost_found_list(request):
    """List lost and found items"""
    items = LostFoundItem.objects.filter(status='active').select_related('posted_by')
    
    item_type = request.GET.get('type')
    if item_type:
        items = items.filter(item_type=item_type)
    
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)
    
    search = request.GET.get('q')
    if search:
        items = items.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
    items = items.order_by('-created_at')
    
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    context = {
        'page_obj': page_obj,
        'item_types': LostFoundItem.ITEM_TYPE_CHOICES,
        'categories': LostFoundItem.CATEGORY_CHOICES,
    }
    return render(request, 'college/lost_found_list.html', context)

@login_required
def lost_found_create(request):
    """Report a lost or found item"""
    if request.method == 'POST':
        form = LostFoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by = request.user
            item.save()
            messages.success(request, 'Your report has been posted!')
            return redirect('college:lost_found_list')
    else:
        form = LostFoundItemForm()
    
    context = {'form': form}
    return render(request, 'college/lost_found_form.html', context)

@login_required
def lost_found_detail(request, pk):
    """View lost/found item details"""
    item = get_object_or_404(LostFoundItem, pk=pk)
    item.view_count += 1
    item.save()
    
    matches = LostFoundMatch.objects.filter(
        Q(lost_item=item) | Q(found_item=item)
    ).select_related('lost_item', 'found_item')
    
    context = {
        'item': item,
        'matches': matches,
    }
    return render(request, 'college/lost_found_detail.html', context)

# ============ COMPLAINTS ============

def complaint_list(request):
    """List all complaints"""
    complaints = Complaint.objects.select_related('posted_by', 'assigned_to')
    
    if not request.user.is_staff:
        complaints = complaints.filter(Q(posted_by=request.user) | Q(is_anonymous=False))
    
    status = request.GET.get('status')
    if status:
        complaints = complaints.filter(status=status)
    
    search = request.GET.get('q')
    if search:
        complaints = complaints.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
    complaints = complaints.order_by('-created_at')
    
    paginator = Paginator(complaints, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    context = {
        'page_obj': page_obj,
        'statuses': Complaint.STATUS_CHOICES,
    }
    return render(request, 'college/complaint_list.html', context)

@login_required
def complaint_create(request):
    """Create a complaint or suggestion"""
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.posted_by = request.user
            complaint.save()
            messages.success(request, 'Your complaint has been submitted!')
            return redirect('college:complaint_list')
    else:
        form = ComplaintForm()
    
    context = {'form': form}
    return render(request, 'college/complaint_form.html', context)

@login_required
def complaint_detail(request, pk):
    """View complaint details"""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Check permissions
    if not (complaint.posted_by == request.user or request.user.is_staff):
        messages.error(request, 'You do not have permission to view this complaint.')
        return redirect('college:complaint_list')
    
    context = {'complaint': complaint}
    return render(request, 'college/complaint_detail.html', context)

# ============ FACULTY DIRECTORY ============

def faculty_list(request):
    """List all faculty members"""
    faculty = FacultyProfile.objects.select_related('user').filter(is_verified=True)
    
    department = request.GET.get('department')
    if department:
        faculty = faculty.filter(department=department)
    
    search = request.GET.get('q')
    if search:
        faculty = faculty.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(subjects__icontains=search)
        )
    
    faculty = faculty.order_by('user__first_name')
    
    paginator = Paginator(faculty, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    departments = FacultyProfile.objects.values_list('department', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'departments': departments,
        'search_query': search,
    }
    return render(request, 'college/faculty_list.html', context)

def faculty_detail(request, pk):
    """View faculty profile"""
    faculty = get_object_or_404(FacultyProfile, pk=pk, is_verified=True)
    
    context = {'faculty': faculty}
    return render(request, 'college/faculty_detail.html', context)

# ============ CAMPUS MAP ============

def campus_map(request):
    """View campus map"""
    locations = CampusLocation.objects.all()
    
    building_type = request.GET.get('type')
    if building_type:
        locations = locations.filter(building_type=building_type)
    
    search = request.GET.get('q')
    if search:
        locations = locations.filter(Q(name__icontains=search) | Q(description__icontains=search))
    
    types = CampusLocation.BUILDING_TYPE_CHOICES
    
    context = {
        'locations': locations,
        'types': types,
    }
    return render(request, 'college/campus_map.html', context)

def campus_location_detail(request, slug):
    """View location details"""
    location = get_object_or_404(CampusLocation, slug=slug)
    nearby = location.nearby.select_related('nearby_location')
    
    context = {
        'location': location,
        'nearby': nearby,
    }
    return render(request, 'college/campus_location_detail.html', context)
