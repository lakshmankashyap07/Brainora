from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, Http404

from .models import Resource
from .forms import ResourceForm

@login_required
def resource_list_view(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'latest')
    
    resources = Resource.objects.all()
    
    # 1. Search Query
    if query:
        resources = resources.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        
    # 2. Category Filter
    if category_filter:
        resources = resources.filter(category=category_filter)
        
    # 3. Sorting
    if sort_by == 'likes':
        resources = resources.annotate(likes_cnt=Count('likes')).order_by('-likes_cnt', '-created_at')
    elif sort_by == 'downloads':
        resources = resources.order_by('-downloads', '-created_at')
    else:
        resources = resources.order_by('-created_at')
        
    # 4. Pagination (9 per page)
    paginator = Paginator(resources, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category_choices': [c[0] for c in Resource.CATEGORY_CHOICES],
        'selected_category': category_filter,
        'selected_sort': sort_by,
        'search_query': query,
    }
    return render(request, 'resources/list.html', context)

@login_required
def resource_detail_view(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    has_liked = request.user in resource.likes.all()
    has_bookmarked = request.user in resource.bookmarks.all()
    
    context = {
        'resource': resource,
        'has_liked': has_liked,
        'has_bookmarked': has_bookmarked,
    }
    return render(request, 'resources/detail.html', context)

@login_required
def upload_resource_view(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            messages.success(request, "Resource uploaded successfully!")
            return redirect('resources:list')
    else:
        form = ResourceForm()
    return render(request, 'resources/upload.html', {'form': form})

@login_required
def like_resource_view(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    user = request.user
    if user in resource.likes.all():
        resource.likes.remove(user)
    else:
        resource.likes.add(user)
    return redirect('resources:detail', pk=pk)

@login_required
def bookmark_resource_view(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    user = request.user
    if user in resource.bookmarks.all():
        resource.bookmarks.remove(user)
    else:
        resource.bookmarks.add(user)
    return redirect('resources:detail', pk=pk)

@login_required
def download_resource_view(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    resource.downloads += 1
    resource.save()
    
    if resource.file:
        return redirect(resource.file.url)
    elif resource.external_link:
        return redirect(resource.external_link)
    
    messages.error(request, "Resource link is broken or unavailable.")
    return redirect('resources:detail', pk=pk)

@login_required
def delete_resource_view(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if resource.uploaded_by != request.user and request.user.role != 'Admin':
        messages.error(request, "You do not have permission to delete this file.")
        return redirect('resources:detail', pk=pk)
        
    resource.delete()
    messages.success(request, "Resource file deleted successfully.")
    return redirect('resources:list')
