from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Course
from resources.models import Resource

@login_required
def course_list_view(request):
    semester_query = request.GET.get('semester', '')
    courses = Course.objects.all().order_by('course_code')
    
    if semester_query:
        courses = courses.filter(semester=semester_query)
        
    context = {
        'courses': courses,
        'semester_choices': range(1, 9),
        'selected_semester': semester_query,
    }
    return render(request, 'courses/list.html', context)

@login_required
def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    papers = course.papers.all().order_by('-year')
    
    # Intelligently query resources matching course code in title/description
    related_resources = Resource.objects.filter(
        Q(title__icontains=course.course_code) | 
        Q(description__icontains=course.course_code)
    ).exclude(category='Previous Year Papers').order_by('-created_at')
    
    context = {
        'course': course,
        'papers': papers,
        'related_resources': related_resources,
    }
    return render(request, 'courses/detail.html', context)
