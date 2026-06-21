from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import PreviousYearPaper
from courses.models import Course

@login_required
def paper_list_view(request):
    course_filter = request.GET.get('course', '')
    type_filter = request.GET.get('type', '')
    year_filter = request.GET.get('year', '')
    query = request.GET.get('q', '')
    
    papers = PreviousYearPaper.objects.all().order_by('-year', '-created_at')
    
    if course_filter:
        papers = papers.filter(course_id=course_filter)
        
    if type_filter:
        papers = papers.filter(paper_type=type_filter)
        
    if year_filter:
        papers = papers.filter(year=year_filter)
        
    if query:
        papers = papers.filter(
            Q(title__icontains=query) | 
            Q(course__course_code__icontains=query) | 
            Q(course__title__icontains=query)
        )
        
    # Get distinct years and all courses for filter dropdowns
    years = PreviousYearPaper.objects.values_list('year', flat=True).distinct().order_by('-year')
    courses = Course.objects.all().order_by('course_code')
    
    context = {
        'papers': papers,
        'courses': courses,
        'years': years,
        'paper_types': [t[0] for t in PreviousYearPaper.PAPER_TYPE_CHOICES],
        'selected_course': course_filter,
        'selected_type': type_filter,
        'selected_year': year_filter,
        'search_query': query,
    }
    return render(request, 'papers/list.html', context)
