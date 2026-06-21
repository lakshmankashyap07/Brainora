from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, FileResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.decorators.http import require_http_methods
from .models import (
    AcademicResource, AcademicResourceDownload, AcademicResourceBookmark,
    AcademicResourceLike, AcademicResourceReport, Syllabus,
    AcademicCalendar, TimeTable
)
from .forms import AcademicResourceForm  # We'll create this
import mimetypes
import os

# ============ RESOURCE MANAGEMENT ============

def resource_list(request):
    """List all academic resources with filtering and search"""
    resources = AcademicResource.objects.filter(status='approved')
    
    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    # Filters
    resource_type = request.GET.get('type', '')
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    
    semester = request.GET.get('semester', '')
    if semester:
        resources = resources.filter(semester=semester)
    
    department = request.GET.get('department', '')
    if department:
        resources = resources.filter(department=department)
    
    # Sorting
    sort_by = request.GET.get('sort', '-uploaded_at')
    if sort_by in ['downloaded', 'liked', 'viewed', 'recent']:
        if sort_by == 'downloaded':
            resources = resources.order_by('-download_count')
        elif sort_by == 'liked':
            resources = resources.order_by('-like_count')
        elif sort_by == 'viewed':
            resources = resources.order_by('-view_count')
        else:
            resources = resources.order_by('-uploaded_at')
    
    # Pagination
    paginator = Paginator(resources, 12)
    page = request.GET.get('page', 1)
    resources_page = paginator.get_page(page)
    
    context = {
        'resources': resources_page,
        'search_query': search_query,
        'resource_types': AcademicResource.RESOURCE_TYPE_CHOICES,
        'semesters': range(1, 9),
    }
    return render(request, 'academic/resource_list.html', context)


@login_required
def upload_resource(request):
    """Upload new academic resource"""
    if request.method == 'POST':
        form = AcademicResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            return redirect('academic:resource_detail', pk=resource.pk)
    else:
        form = AcademicResourceForm()
    
    return render(request, 'academic/upload_resource.html', {'form': form})


def resource_detail(request, pk):
    """View resource details"""
    resource = get_object_or_404(AcademicResource, pk=pk, status='approved')
    
    # Increment view count
    resource.view_count += 1
    resource.save()
    
    # Check if user has bookmarked
    is_bookmarked = False
    is_liked = False
    if request.user.is_authenticated:
        is_bookmarked = AcademicResourceBookmark.objects.filter(
            resource=resource, user=request.user
        ).exists()
        is_liked = AcademicResourceLike.objects.filter(
            resource=resource, user=request.user
        ).exists()
    
    # Get recommendations (similar resources)
    similar = AcademicResource.objects.filter(
        status='approved',
        subject=resource.subject,
        semester=resource.semester
    ).exclude(pk=pk)[:6]
    
    context = {
        'resource': resource,
        'is_bookmarked': is_bookmarked,
        'is_liked': is_liked,
        'similar': similar,
    }
    return render(request, 'academic/resource_detail.html', context)


@login_required
def download_resource(request, pk):
    """Download resource file"""
    resource = get_object_or_404(AcademicResource, pk=pk, status='approved')
    
    # Log download
    AcademicResourceDownload.objects.get_or_create(
        resource=resource,
        user=request.user
    )
    resource.download_count += 1
    resource.save()
    
    # Serve file
    if resource.file:
        response = FileResponse(resource.file.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(resource.file.name)}"'
        return response
    
    return HttpResponseForbidden("File not found")


@login_required
@require_http_methods(["POST"])
def bookmark_resource(request, pk):
    """Bookmark/unbookmark a resource"""
    resource = get_object_or_404(AcademicResource, pk=pk)
    
    bookmark, created = AcademicResourceBookmark.objects.get_or_create(
        resource=resource,
        user=request.user
    )
    
    if not created:
        bookmark.delete()
        return JsonResponse({'bookmarked': False, 'message': 'Bookmark removed'})
    
    return JsonResponse({'bookmarked': True, 'message': 'Resource bookmarked'})


@login_required
@require_http_methods(["POST"])
def like_resource(request, pk):
    """Like/unlike a resource"""
    resource = get_object_or_404(AcademicResource, pk=pk)
    
    like, created = AcademicResourceLike.objects.get_or_create(
        resource=resource,
        user=request.user
    )
    
    if not created:
        like.delete()
        resource.like_count -= 1
        resource.save()
        return JsonResponse({'liked': False, 'count': resource.like_count})
    
    resource.like_count += 1
    resource.save()
    return JsonResponse({'liked': True, 'count': resource.like_count})


@login_required
def report_resource(request, pk):
    """Report a resource for inappropriate content"""
    resource = get_object_or_404(AcademicResource, pk=pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description')
        
        AcademicResourceReport.objects.create(
            resource=resource,
            reported_by=request.user,
            reason=reason,
            description=description
        )
        return JsonResponse({'success': True, 'message': 'Resource reported successfully'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def edit_resource(request, pk):
    """Edit own resource"""
    resource = get_object_or_404(AcademicResource, pk=pk)
    
    # Only owner or admin can edit
    if resource.uploaded_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to edit this resource")
    
    if request.method == 'POST':
        form = AcademicResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('academic:resource_detail', pk=resource.pk)
    else:
        form = AcademicResourceForm(instance=resource)
    
    return render(request, 'academic/edit_resource.html', {'form': form, 'resource': resource})


@login_required
def delete_resource(request, pk):
    """Delete own resource"""
    resource = get_object_or_404(AcademicResource, pk=pk)
    
    # Only owner or admin can delete
    if resource.uploaded_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to delete this resource")
    
    if request.method == 'POST':
        resource.delete()
        return redirect('academic:resource_list')
    
    return render(request, 'academic/confirm_delete.html', {'resource': resource})


# ============ SYLLABUS ============

def syllabus_list(request):
    """List all syllabus documents"""
    syllabi = Syllabus.objects.all()
    
    semester = request.GET.get('semester')
    if semester:
        syllabi = syllabi.filter(semester=semester)
    
    department = request.GET.get('department')
    if department:
        syllabi = syllabi.filter(department=department)
    
    context = {
        'syllabi': syllabi,
        'semesters': range(1, 9),
    }
    return render(request, 'academic/syllabus_list.html', context)


def syllabus_detail(request, pk):
    """View syllabus"""
    syllabus = get_object_or_404(Syllabus, pk=pk)
    return render(request, 'academic/syllabus_detail.html', {'syllabus': syllabus})


# ============ ACADEMIC CALENDAR ============

def calendar_view(request):
    """View academic calendar"""
    events = AcademicCalendar.objects.all().order_by('event_date')
    
    context = {
        'events': events,
    }
    return render(request, 'academic/calendar.html', context)


# ============ TIMETABLE ============

def timetable_view(request):
    """View timetable"""
    semester = request.GET.get('semester', 1)
    department = request.GET.get('department', '')
    
    timetables = TimeTable.objects.filter(semester=semester)
    if department:
        timetables = timetables.filter(department=department)
    
    # Group by day
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    schedule = {}
    for day in days:
        schedule[day] = list(timetables.filter(day=day).order_by('time_slot'))
    
    context = {
        'schedule': schedule,
        'semester': semester,
        'semesters': range(1, 9),
    }
    return render(request, 'academic/timetable.html', context)


def timetable_semester(request, semester):
    """View timetable for specific semester"""
    return timetable_view(request)
