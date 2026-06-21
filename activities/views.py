from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import CollegeActivity

@login_required
def activity_list_view(request):
    type_filter = request.GET.get('type', '')
    query = request.GET.get('q', '')
    
    activities = CollegeActivity.objects.all().order_by('-activity_date')
    
    if type_filter:
        activities = activities.filter(activity_type=type_filter)
        
    if query:
        activities = activities.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )
        
    context = {
        'activities': activities,
        'activity_types': [t[0] for t in CollegeActivity.ACTIVITY_TYPE_CHOICES],
        'selected_type': type_filter,
        'search_query': query,
    }
    return render(request, 'activities/list.html', context)
