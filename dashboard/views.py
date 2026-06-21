from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from courses.models import Course
from resources.models import Resource
from papers.models import PreviousYearPaper
from activities.models import CollegeActivity

@login_required
def home_view(request):
    user = request.user
    
    # 1. Capture search & filter query params
    query = request.GET.get('q', '')
    semester_filter = request.GET.get('semester', '')
    category_filter = request.GET.get('category', '')
    paper_type_filter = request.GET.get('paper_type', '')
    
    # 2. General Portal Statistics
    courses_count = Course.objects.count()
    resources_count = Resource.objects.count()
    papers_count = PreviousYearPaper.objects.count()
    bookmarks_count = user.bookmarked_resources.count()
    
    # 3. Chart.js statistics (uploads by category)
    category_counts = Resource.objects.values('category').annotate(count=Count('id'))
    chart_labels = [item['category'] for item in category_counts]
    chart_values = [item['count'] for item in category_counts]
    
    # If no data exists, supply defaults so Chart.js renders beautifully
    if not chart_labels:
        chart_labels = ['Notes', 'Assignments', 'Lab Files', 'Roadmaps']
        chart_values = [0, 0, 0, 0]
        
    # 4. Fetch content blocks
    # Trending: ordered by likes count, then downloads count
    trending_resources = Resource.objects.annotate(likes_cnt=Count('likes')).order_by('-likes_cnt', '-downloads')
    
    # Recent Uploads
    recent_resources = Resource.objects.all().order_by('-created_at')
    
    # Upcoming Events / Deadlines
    upcoming_activities = CollegeActivity.objects.filter(
        activity_type__in=['Event', 'Deadline'],
        activity_date__gte=timezone.now().date()
    ).order_by('activity_date')
    
    # Latest Notices / Announcements / Holidays
    latest_announcements = CollegeActivity.objects.filter(
        activity_type__in=['Announcement', 'Notice', 'Holiday']
    ).order_by('-created_at')
    
    # 5. Apply global search / filters if supplied
    search_active = False
    search_courses = None
    search_resources = None
    search_papers = None
    search_activities = None
    
    if query or semester_filter or category_filter or paper_type_filter:
        search_active = True
        
        # Courses Search
        courses_qs = Course.objects.all()
        if query:
            courses_qs = courses_qs.filter(Q(course_code__icontains=query) | Q(title__icontains=query) | Q(instructor__icontains=query))
        if semester_filter:
            courses_qs = courses_qs.filter(semester=semester_filter)
        search_courses = courses_qs[:10]
        
        # Resources Search
        resources_qs = Resource.objects.all()
        if query:
            resources_qs = resources_qs.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if category_filter:
            resources_qs = resources_qs.filter(category=category_filter)
        search_resources = resources_qs[:10]
        
        # Papers Search
        papers_qs = PreviousYearPaper.objects.all()
        if query:
            papers_qs = papers_qs.filter(Q(title__icontains=query) | Q(course__course_code__icontains=query) | Q(course__title__icontains=query))
        if paper_type_filter:
            papers_qs = papers_qs.filter(paper_type=paper_type_filter)
        search_papers = papers_qs[:10]
        
        # Activities Search
        activities_qs = CollegeActivity.objects.all()
        if query:
            activities_qs = activities_qs.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))
        search_activities = activities_qs[:10]
        
    context = {
        'courses_count': courses_count,
        'resources_count': resources_count,
        'papers_count': papers_count,
        'bookmarks_count': bookmarks_count,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'trending_resources': trending_resources[:5],
        'recent_resources': recent_resources[:5],
        'upcoming_activities': upcoming_activities[:5],
        'latest_announcements': latest_announcements[:5],
        
        # Search parameters
        'search_active': search_active,
        'search_query': query,
        'search_courses': search_courses,
        'search_resources': search_resources,
        'search_papers': search_papers,
        'search_activities': search_activities,
        
        # Choice dropdown values
        'category_choices': [c[0] for c in Resource.CATEGORY_CHOICES],
        'paper_choices': [p[0] for p in PreviousYearPaper.PAPER_TYPE_CHOICES],
        'semester_choices': range(1, 9),
    }
    
    return render(request, 'dashboard/home.html', context)

@login_required
def notifications_view(request):
    # Retrieve activities of type Notice / Announcement to serve as notifications
    notices = CollegeActivity.objects.filter(
        activity_type__in=['Announcement', 'Notice'],
        created_at__gte=timezone.now() - timezone.timedelta(days=14)
    ).order_by('-created_at')
    return render(request, 'dashboard/notifications.html', {'notifications': notices})
