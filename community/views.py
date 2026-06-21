from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.decorators.http import require_http_methods
from .models import (
    ForumCategory, ForumPost, ForumPostComment, ForumPostLike,
    Question, Answer, QuestionVote,
    StudyGroup, StudyGroupMember, StudyGroupResource,
    LiveStudyRoom, LiveStudyRoomMember, LiveStudyRoomMessage,
    UserProfile, UserFollow, CommunityNotification, ActivityFeed
)

# ============ FORUM ============

def forum_list(request):
    """List all forum posts"""
    posts = ForumPost.objects.select_related('category', 'author').prefetch_related('comments')
    
    search_query = request.GET.get('q', '')
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category_id=category)
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page', 1)
    posts_page = paginator.get_page(page)
    
    categories = ForumCategory.objects.all()
    
    context = {
        'posts': posts_page,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'community/forum_list.html', context)


def forum_category(request, category_id):
    """View posts in specific category"""
    category = get_object_or_404(ForumCategory, pk=category_id)
    posts = category.posts.all()
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page', 1)
    posts_page = paginator.get_page(page)
    
    context = {
        'category': category,
        'posts': posts_page,
    }
    return render(request, 'community/forum_category.html', context)


@login_required
def create_post(request):
    """Create a new forum post"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        
        post = ForumPost.objects.create(
            title=title,
            content=content,
            category_id=category_id,
            author=request.user
        )
        
        return redirect('community:post_detail', pk=post.pk)
    
    categories = ForumCategory.objects.all()
    return render(request, 'community/create_post.html', {'categories': categories})


def post_detail(request, pk):
    """View post details"""
    post = get_object_or_404(ForumPost, pk=pk)
    post.views += 1
    post.save()
    
    comments = post.comments.select_related('author')
    
    is_liked = False
    if request.user.is_authenticated:
        is_liked = ForumPostLike.objects.filter(post=post, user=request.user).exists()
    
    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
    }
    return render(request, 'community/post_detail.html', context)


@login_required
def edit_post(request, pk):
    """Edit post"""
    post = get_object_or_404(ForumPost, pk=pk)
    
    if post.author != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        post.save()
        return redirect('community:post_detail', pk=post.pk)
    
    return render(request, 'community/edit_post.html', {'post': post})


@login_required
def delete_post(request, pk):
    """Delete post"""
    post = get_object_or_404(ForumPost, pk=pk)
    
    if post.author != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        post.delete()
        return redirect('community:forum_list')
    
    return render(request, 'community/confirm_delete.html', {'post': post})


@login_required
def add_comment(request, pk):
    """Add comment to post"""
    post = get_object_or_404(ForumPost, pk=pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = ForumPostComment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        post.comment_count += 1
        post.save()
        return redirect('community:post_detail', pk=post.pk)
    
    return JsonResponse({'success': False})


@login_required
@require_http_methods(["POST"])
def like_post(request, pk):
    """Like/unlike a post"""
    post = get_object_or_404(ForumPost, pk=pk)
    
    like, created = ForumPostLike.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
        post.like_count -= 1
        post.save()
        return JsonResponse({'liked': False, 'count': post.like_count})
    
    post.like_count += 1
    post.save()
    return JsonResponse({'liked': True, 'count': post.like_count})


# ============ QUESTIONS & ANSWERS ============

def questions_list(request):
    """List all questions"""
    questions = Question.objects.select_related('author')
    
    search_query = request.GET.get('q', '')
    if search_query:
        questions = questions.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
    
    tag = request.GET.get('tag')
    if tag:
        questions = questions.filter(tags__icontains=tag)
    
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'popular':
        questions = questions.annotate(answer_count=Count('answers')).order_by('-answer_count')
    else:
        questions = questions.order_by('-created_at')
    
    paginator = Paginator(questions, 10)
    page = request.GET.get('page', 1)
    questions_page = paginator.get_page(page)
    
    context = {
        'questions': questions_page,
        'search_query': search_query,
    }
    return render(request, 'community/questions_list.html', context)


@login_required
def ask_question(request):
    """Ask a new question"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags', '')
        
        question = Question.objects.create(
            title=title,
            content=content,
            tags=tags,
            author=request.user
        )
        
        return redirect('community:question_detail', pk=question.pk)
    
    return render(request, 'community/ask_question.html')


def question_detail(request, pk):
    """View question and answers"""
    question = get_object_or_404(Question, pk=pk)
    question.views += 1
    question.save()
    
    answers = question.answers.select_related('author')
    
    context = {
        'question': question,
        'answers': answers,
    }
    return render(request, 'community/question_detail.html', context)


@login_required
def answer_question(request, pk):
    """Post an answer to a question"""
    question = get_object_or_404(Question, pk=pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        answer = Answer.objects.create(
            question=question,
            author=request.user,
            content=content
        )
        question.is_answered = True
        question.save()
        return redirect('community:question_detail', pk=question.pk)
    
    return render(request, 'community/answer_question.html', {'question': question})


@login_required
@require_http_methods(["POST"])
def vote_answer(request, pk):
    """Vote on an answer"""
    answer = get_object_or_404(Answer, pk=pk)
    vote_type = request.POST.get('vote_type')  # 'upvote' or 'downvote'
    
    existing_vote = QuestionVote.objects.filter(answer=answer, user=request.user).first()
    
    if existing_vote:
        existing_vote.delete()
        if existing_vote.vote_type == 'upvote':
            answer.upvote_count -= 1
        else:
            answer.downvote_count -= 1
    
    if vote_type in ['upvote', 'downvote']:
        QuestionVote.objects.create(answer=answer, user=request.user, vote_type=vote_type)
        if vote_type == 'upvote':
            answer.upvote_count += 1
        else:
            answer.downvote_count += 1
    
    answer.save()
    return JsonResponse({'upvotes': answer.upvote_count, 'downvotes': answer.downvote_count})


@login_required
@require_http_methods(["POST"])
def accept_answer(request, pk):
    """Mark answer as accepted"""
    answer = get_object_or_404(Answer, pk=pk)
    
    if answer.question.author != request.user:
        return JsonResponse({'success': False, 'message': 'Only question author can accept answer'}, status=403)
    
    answer.is_accepted = not answer.is_accepted
    answer.save()
    
    return JsonResponse({'success': True, 'accepted': answer.is_accepted})


# ============ STUDY GROUPS ============

def study_groups_list(request):
    """List all study groups"""
    groups = StudyGroup.objects.annotate(member_count=Count('members'))
    
    search_query = request.GET.get('q', '')
    if search_query:
        groups = groups.filter(
            Q(name__icontains=search_query) | Q(topic__icontains=search_query)
        )
    
    paginator = Paginator(groups, 12)
    page = request.GET.get('page', 1)
    groups_page = paginator.get_page(page)
    
    context = {
        'groups': groups_page,
        'search_query': search_query,
    }
    return render(request, 'community/study_groups_list.html', context)


@login_required
def create_study_group(request):
    """Create a new study group"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        topic = request.POST.get('topic')
        is_private = request.POST.get('is_private') == 'on'
        
        group = StudyGroup.objects.create(
            name=name,
            description=description,
            topic=topic,
            is_private=is_private,
            created_by=request.user
        )
        group.admins.add(request.user)
        StudyGroupMember.objects.create(group=group, user=request.user)
        
        return redirect('community:study_group_detail', pk=group.pk)
    
    return render(request, 'community/create_study_group.html')


def study_group_detail(request, pk):
    """View study group details"""
    group = get_object_or_404(StudyGroup, pk=pk)
    members = group.members.all()
    resources = group.resources.all()
    
    is_member = False
    if request.user.is_authenticated:
        is_member = StudyGroupMember.objects.filter(group=group, user=request.user).exists()
    
    context = {
        'group': group,
        'members': members,
        'resources': resources,
        'is_member': is_member,
    }
    return render(request, 'community/study_group_detail.html', context)


@login_required
def join_study_group(request, pk):
    """Join a study group"""
    group = get_object_or_404(StudyGroup, pk=pk)
    
    if not StudyGroupMember.objects.filter(group=group, user=request.user).exists():
        StudyGroupMember.objects.create(group=group, user=request.user)
    
    return redirect('community:study_group_detail', pk=group.pk)


@login_required
def leave_study_group(request, pk):
    """Leave a study group"""
    group = get_object_or_404(StudyGroup, pk=pk)
    StudyGroupMember.objects.filter(group=group, user=request.user).delete()
    
    return redirect('community:study_groups_list')


# ============ LIVE STUDY ROOMS ============

def live_rooms_list(request):
    """List active live study rooms"""
    rooms = LiveStudyRoom.objects.filter(status='active')
    
    paginator = Paginator(rooms, 12)
    page = request.GET.get('page', 1)
    rooms_page = paginator.get_page(page)
    
    context = {'rooms': rooms_page}
    return render(request, 'community/live_rooms_list.html', context)


@login_required
def create_live_room(request):
    """Create a live study room"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = int(request.POST.get('duration', 60))
        
        from django.utils import timezone
        from datetime import timedelta
        
        room = LiveStudyRoom.objects.create(
            title=title,
            description=description,
            creator=request.user,
            session_duration=duration,
            started_at=timezone.now()
        )
        LiveStudyRoomMember.objects.create(room=room, user=request.user)
        
        return redirect('community:live_room_detail', pk=room.pk)
    
    return render(request, 'community/create_live_room.html')


def live_room_detail(request, pk):
    """View live room"""
    room = get_object_or_404(LiveStudyRoom, pk=pk)
    members = room.room_members.all()
    messages = room.messages.select_related('sender')
    
    is_member = False
    if request.user.is_authenticated:
        is_member = LiveStudyRoomMember.objects.filter(room=room, user=request.user).exists()
    
    context = {
        'room': room,
        'members': members,
        'messages': messages,
        'is_member': is_member,
    }
    return render(request, 'community/live_room_detail.html', context)


@login_required
def join_live_room(request, pk):
    """Join a live room"""
    room = get_object_or_404(LiveStudyRoom, pk=pk)
    
    if not LiveStudyRoomMember.objects.filter(room=room, user=request.user).exists():
        LiveStudyRoomMember.objects.create(room=room, user=request.user)
        room.current_members += 1
        room.save()
    
    return redirect('community:live_room_detail', pk=room.pk)


@login_required
def leave_live_room(request, pk):
    """Leave a live room"""
    room = get_object_or_404(LiveStudyRoom, pk=pk)
    
    from django.utils import timezone
    member = LiveStudyRoomMember.objects.filter(room=room, user=request.user).first()
    if member:
        member.left_at = timezone.now()
        member.save()
        room.current_members = max(0, room.current_members - 1)
        room.save()
    
    return redirect('community:live_rooms_list')


# ============ USER PROFILES ============

def user_profile(request, user_id):
    """View user profile"""
    from authentication.models import CustomUser
    user = get_object_or_404(CustomUser, pk=user_id)
    
    is_following = False
    if request.user.is_authenticated:
        is_following = UserFollow.objects.filter(
            follower=request.user,
            following=user
        ).exists()
    
    posts = user.forum_posts.all()
    questions = user.questions_asked.all()
    
    context = {
        'profile_user': user,
        'is_following': is_following,
        'posts': posts,
        'questions': questions,
    }
    return render(request, 'community/user_profile.html', context)


@login_required
@require_http_methods(["POST"])
def follow_user(request, user_id):
    """Follow/unfollow a user"""
    from authentication.models import CustomUser
    user = get_object_or_404(CustomUser, pk=user_id)
    
    if user == request.user:
        return JsonResponse({'success': False, 'message': "Can't follow yourself"})
    
    follow, created = UserFollow.objects.get_or_create(
        follower=request.user,
        following=user
    )
    
    if not created:
        follow.delete()
        return JsonResponse({'following': False})
    
    return JsonResponse({'following': True})


def notifications_list(request):
    """View user notifications"""
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    notifications = CommunityNotification.objects.filter(user=request.user)
    
    paginator = Paginator(notifications, 15)
    page = request.GET.get('page', 1)
    notifications_page = paginator.get_page(page)
    
    context = {'notifications': notifications_page}
    return render(request, 'community/notifications_list.html', context)
