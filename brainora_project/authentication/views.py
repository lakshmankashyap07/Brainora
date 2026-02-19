from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import LoginForm, SignUpForm, ResourceUploadForm, EditProfileForm
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
    """Handle user login and signup on unified page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    login_form = LoginForm()
    signup_form = SignUpForm()
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'login')
        
        if form_type == 'signup':
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, 'Account created successfully! Welcome to Brainora.')
                return redirect('dashboard')
            else:
                for field, errors in signup_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{error}')
        else:
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username/email or password.')
    
    return render(request, 'authentication/login.html', {
        'login_form': login_form,
        'signup_form': signup_form
    })


def signup_view(request):
    """Redirect to login page where both signup and login are available"""
    return redirect('login')


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
def upload_page_view(request):
    """Render a dedicated upload page where users can upload category-wise resources."""
    # allow optional preselected category via query param
    category = request.GET.get('category', '')
    form = ResourceUploadForm(initial={'category': category})
    context = {
        'resource_form': form,
        'preselected_category': category,
    }
    return render(request, 'authentication/upload.html', context)


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
    if course_filter and course_filter.isdigit():
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
def resource_list_view(request, category_slug):
    """List resources for a given category (by slug)."""
    # Normalize title for display
    category_title = dict(Resource.CATEGORY_CHOICES).get(category_slug, category_slug.replace('-', ' ').title())

    # Base queryset filtered by category
    resources = Resource.objects.filter(category=category_slug).order_by('-created_at')

    # Optional search
    search_query = request.GET.get('search', '').strip()
    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    context = {
        'resources': resources,
        'category_title': category_title,
        'category_slug': category_slug,
        'search_query': search_query,
    }
    return render(request, 'pages/resource_list.html', context)


@login_required(login_url='login')
def delete_resource_view(request, pk):
    """Delete a resource if the requesting user is the uploader or a superuser."""
    res = get_object_or_404(Resource, pk=pk)

    # Authorization: only uploader or admin can delete
    if not (request.user == res.uploaded_by or request.user.is_superuser):
        messages.error(request, 'You are not authorized to delete this resource.')
        return redirect('dashboard')

    if request.method == 'POST':
        # If there's an uploaded file, remove it from storage first
        try:
            if res.file:
                res.file.delete(save=False)
        except Exception:
            pass

        # Get the category for redirect
        category = res.category

        res.delete()
        messages.success(request, 'Resource deleted successfully.')
        # Redirect to the resource list page for that category
        return redirect('resource_list', category_slug=category)

    # Show confirmation page for non-POST requests
    return render(request, 'authentication/delete_confirm.html', {
        'object': res, 
        'type': 'Resource'
    })


@login_required(login_url='login')
def delete_paper_view(request, pk):
    """Allow uploader or admin to delete a PreviousYearPaper."""
    paper = get_object_or_404(PreviousYearPaper, pk=pk)
    if not (request.user == paper.uploaded_by or request.user.is_superuser):
        messages.error(request, 'You are not authorized to delete this paper.')
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    if request.method == 'POST':
        try:
            if paper.file:
                paper.file.delete(save=False)
        except Exception:
            pass
        paper.delete()
        messages.success(request, 'Paper deleted successfully.')
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    return render(request, 'authentication/delete_confirm.html', {
        'object': paper, 
        'type': 'Paper'
    })


@login_required(login_url='login')
def delete_activity_view(request, pk):
    """Allow creator or admin to delete an activity."""
    activity = get_object_or_404(CollegeActivity, pk=pk)
    if not (request.user == activity.created_by or request.user.is_superuser):
        messages.error(request, 'You are not authorized to delete this activity.')
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    if request.method == 'POST':
        # no files attached usually
        activity.delete()
        messages.success(request, 'Activity deleted successfully.')
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    return render(request, 'authentication/delete_confirm.html', {
        'object': activity, 
        'type': 'Activity'
    })

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

def privacy_policy_view(request):
    """Display privacy policy page"""
    return render(request, 'pages/privacy_policy.html')


def about_view(request):
    """Display about page with team information"""
    return render(request, 'pages/about.html')



def team_member_view(request, member):
    """Display a team member detail page based on member slug"""
    members = {
        'laksh': {
            'name': 'Lakshman kashyap',
            'role': 'Frontend Developer',
            'image': 'images/laksh.jpg',
            'description': (
                'Lakshman Kashyap is a Frontend Developer at Brainora who focuses on designing and developing the visual and interactive parts of the platform. '
                'He works on creating responsive layouts, smooth navigation, and modern UI components to ensure users have an engaging and seamless learning experience across all devices.'
            ),
            'github': 'https://github.com/lakshmankashyap07',
            'linkedin': 'https://www.linkedin.com/in/lakshman-kashyap0/',
            'instagram': 'https://www.instagram.com/lak5hm_n_07/',
        },
        'lucky': {
            'name': 'Lucky Jaiswal',
            'role': 'Backend Developer',
            'image': 'images/lucky.png',
            'description': (
                'Lucky Jaiswal is a Backend Developer responsible for managing the server-side architecture of Brainora. He works on API development, database management, authentication systems, and security implementation to ensure the platform runs efficiently, securely, and reliably.'
            ),
            'github': 'https://github.com/Luckyjaiswa',
            'linkedin': 'https://www.linkedin.com/in/luckyjaiswal98/',
            'instagram': 'https://www.instagram.com/lucky____jaiswal/',
        },
        'mith': {
            'name': 'Mithlesh Kumar',
            'role': 'Backend Developer',
            'image': 'images/mith.png',
            'description': (
                'Mithlesh is a Backend Developer who focuses on backend logic, system integration, and performance optimization. He ensures smooth data handling, scalability, and stability of the platform to support a growing number of learners without compromising speed or security.'
            ),
            'github': 'https://github.com/Mithleshyadavgithub',
            'linkedin': 'https://www.linkedin.com/in/mithlesh-kumar-4ab73929a/',
            'instagram': 'https://www.instagram.com/mithleshyadav876/',
        },
        'kriya': {
            'name': 'Kriya Yadav',
            'role': 'Frontend Developer',
            'image': 'images/kriya.jpg',
            'description': (
                'Kriya Yadav serves as a Frontend Developer, contributing to the design structure and user experience of Brainora. She ensures that the interface is intuitive, visually appealing, and user-friendly while maintaining cross-browser compatibility and overall performance optimization.'
            ),
            'github': 'https://github.com/kriyay3-yadav',
            'linkedin': 'https://www.linkedin.com/in/kriya-yadav-741149334/',
            'instagram': 'https://www.instagram.com/kriyay2525/',
        },
    }

    info = members.get(member)
    if not info:
        return redirect('about')

    context = {
        'member': info,
    }
    return render(request, 'pages/team_member.html', context)


def whatsapp_view(request):
    """Display WhatsApp connect page with Group and Channel options"""
    return render(request, 'pages/whatsapp.html')


def telegram_premium_view(request):
    """Display Telegram Premium page (PIN protected - handled in frontend)"""
    return render(request, 'pages/telegram_premium.html')


@login_required(login_url='login')
def profile_view(request):
    """Display user profile page"""
    context = {
        'user_profile': request.user,
    }
    return render(request, 'authentication/profile.html', context)


@login_required(login_url='login')
def edit_profile_view(request):
    """Handle profile editing"""
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = EditProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user_profile': request.user,
    }
    return render(request, 'authentication/edit_profile.html', context)
