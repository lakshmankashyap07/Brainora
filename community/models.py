from django.db import models
from authentication.models import CustomUser
from django.utils import timezone

# ============ DISCUSSION FORUM ============

class ForumCategory(models.Model):
    """Categories for discussion forum"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Font awesome icon class
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Forum Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ForumPost(models.Model):
    """Discussion forum posts"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(ForumCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='forum_posts')
    
    # Media
    image = models.ImageField(upload_to='forum_posts/', null=True, blank=True)
    attachment = models.FileField(upload_to='forum_attachments/', null=True, blank=True)
    
    # Statistics
    views = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    
    # Status
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title


class ForumPostComment(models.Model):
    """Comments on forum posts"""
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='forum_comments')
    content = models.TextField()
    
    like_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']


class ForumPostLike(models.Model):
    """Like system for forum posts"""
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']


# ============ QUESTION & ANSWER ============

class Question(models.Model):
    """Q&A Section - Like Stack Overflow"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.CharField(max_length=255, help_text="Comma-separated tags")
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='questions_asked')
    views = models.IntegerField(default=0)
    
    # Status
    is_answered = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_answered']),
        ]
    
    def __str__(self):
        return self.title


class Answer(models.Model):
    """Answers to questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='answers_given')
    content = models.TextField()
    
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_accepted', '-upvote_count', 'created_at']


class QuestionVote(models.Model):
    """Upvote/Downvote for answers"""
    VOTE_TYPE = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    ]
    
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['answer', 'user']


# ============ STUDY GROUPS ============

class StudyGroup(models.Model):
    """Virtual study groups for collaborative learning"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    topic = models.CharField(max_length=255)
    
    # Group Settings
    is_private = models.BooleanField(default=False)
    max_members = models.IntegerField(default=50)
    
    # Admin
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_study_groups')
    admins = models.ManyToManyField(CustomUser, related_name='admin_study_groups')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class StudyGroupMember(models.Model):
    """Membership in study groups"""
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='study_groups')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['group', 'user']


class StudyGroupResource(models.Model):
    """Resources shared within a study group"""
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='study_group_resources/')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']


# ============ LIVE STUDY ROOMS ============

class LiveStudyRoom(models.Model):
    """Virtual study rooms with timer and chat"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('ended', 'Ended'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Room Info
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_study_rooms')
    max_members = models.IntegerField(default=20)
    
    # Timer
    session_duration = models.IntegerField(default=60)  # in minutes
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    current_members = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return self.title


class LiveStudyRoomMember(models.Model):
    """Members in a live study room"""
    room = models.ForeignKey(LiveStudyRoom, on_delete=models.CASCADE, related_name='room_members')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['room', 'user']


class LiveStudyRoomMessage(models.Model):
    """Chat messages in live study rooms"""
    room = models.ForeignKey(LiveStudyRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']


# ============ SOCIAL FEATURES ============

class UserProfile(models.Model):
    """Extended user profile for social features"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='social_profile')
    bio = models.TextField(blank=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Social Profile"


class UserFollow(models.Model):
    """Follow relationship between users"""
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['follower', 'following']


class CommunityNotification(models.Model):
    """Notifications for community activities"""
    NOTIFICATION_TYPES = [
        ('new_post', 'New Forum Post'),
        ('new_comment', 'New Comment'),
        ('new_answer', 'New Answer'),
        ('new_like', 'New Like'),
        ('new_follower', 'New Follower'),
        ('group_invite', 'Group Invitation'),
        ('room_invite', 'Room Invitation'),
        ('mention', 'Mention'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='community_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    related_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications_sent')
    is_read = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']


class ActivityFeed(models.Model):
    """Activity feed for user's social network"""
    ACTIVITY_TYPES = [
        ('post', 'Posted'),
        ('answer', 'Answered'),
        ('joined_group', 'Joined Group'),
        ('followed', 'Started Following'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Activity Feeds"
