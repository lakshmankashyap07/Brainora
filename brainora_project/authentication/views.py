from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import LoginForm, SignUpForm, ResourceUploadForm
from .models import Course, PreviousYearPaper, CollegeActivity, Resource


def home_view(request):
    """Home page - displays welcome and key information"""
    upcoming_activities = CollegeActivity.objects.filter(
        activity_type__in=['event', 'deadline']
    ).order_by('date')[:6]
    
    recent_announcements = CollegeActivity.objects.filter(
        activity_type='announcement'
    ).order_by('-created_at')[:5]
    
    total_courses = Course.objects.count()
    
    context = {
        'upcoming_activities': upcoming_activities,
        'recent_announcements': recent_announcements,
        'total_courses': total_courses,
    }
    return render(request, 'pages/home.html', context)


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})


def signup_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Brainora.')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    
    return render(request, 'authentication/signup.html', {'form': form})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required(login_url='login')
def dashboard_view(request):
    """Dashboard view - only for logged in users"""
    user_semester = request.user.semester or 1
    
    # Get courses for user's semester
    courses = Course.objects.filter(semester=user_semester)
    
    # Get recent materials
    recent_papers = PreviousYearPaper.objects.filter(
        course__semester=user_semester
    ).order_by('-created_at')[:5]
    
    # Get upcoming activities
    upcoming_activities = CollegeActivity.objects.filter(
        activity_type__in=['event', 'deadline']
    ).order_by('date')[:5]

    # Resources (all for now; front-end can filter by category)
    resources = Resource.objects.all()[:50]

    # Prepare upload form
    resource_form = ResourceUploadForm()
    
    context = {
        'courses': courses,
        'recent_papers': recent_papers,
        'upcoming_activities': upcoming_activities,
        'resources': resources,
        'resource_form': resource_form,
    }
    return render(request, 'authentication/dashboard.html', context)


@login_required(login_url='login')
def upload_resource_view(request):
    """Handle resource uploads (file or link) from modal"""
    if request.method != 'POST':
        return redirect('dashboard')

    form = ResourceUploadForm(request.POST, request.FILES)
    if form.is_valid():
        res = form.save(commit=False)
        res.uploaded_by = request.user
        res.save()
        messages.success(request, 'Resource uploaded successfully.')
    else:
        for field, errs in form.errors.items():
            for err in errs:
                messages.error(request, f'{field}: {err}')

    return redirect('dashboard')


@login_required(login_url='login')
def courses_view(request):
    """View all courses"""
    user_semester = request.user.semester or 1
    courses = Course.objects.filter(semester=user_semester).order_by('code')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(code__icontains=search_query) | 
            Q(title__icontains=search_query) |
            Q(instructor__icontains=search_query)
        )
    
    context = {
        'courses': courses,
        'search_query': search_query,
        'user_semester': user_semester,
    }
    return render(request, 'pages/courses.html', context)


@login_required(login_url='login')
def course_detail_view(request, course_id):
    """View course details and papers"""
    course = get_object_or_404(Course, pk=course_id)
    papers = course.papers.all().order_by('-year', '-created_at')
    
    context = {
        'course': course,
        'papers': papers,
    }
    return render(request, 'pages/course_detail.html', context)


@login_required(login_url='login')
def papers_view(request):
    """View all previous year papers"""
    user_semester = request.user.semester or 1
    papers = PreviousYearPaper.objects.filter(
        course__semester=user_semester
    ).order_by('-year', '-created_at')
    
    # Filter by paper type
    paper_type = request.GET.get('type', '')
    if paper_type:
        papers = papers.filter(paper_type=paper_type)
    
    # Filter by course
    course_filter = request.GET.get('course', '')
    if course_filter:
        papers = papers.filter(course_id=course_filter)
    
    # Get available courses for filter
    courses = Course.objects.filter(semester=user_semester)
    
    context = {
        'papers': papers,
        'courses': courses,
        'selected_type': paper_type,
        'selected_course': course_filter,
    }
    return render(request, 'pages/papers.html', context)


@login_required(login_url='login')
def activities_view(request):
    """View college activities and updates"""
    activities = CollegeActivity.objects.all().order_by('-date')
    
    # Filter by activity type
    activity_type = request.GET.get('type', '')
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    
    context = {
        'activities': activities,
        'selected_type': activity_type,
    }
    return render(request, 'pages/activities.html', context)
