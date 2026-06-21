from django.contrib import admin
from .models import (
    ForumCategory, ForumPost, ForumPostComment, ForumPostLike,
    Question, Answer, QuestionVote,
    StudyGroup, StudyGroupMember, StudyGroupResource,
    LiveStudyRoom, LiveStudyRoomMember, LiveStudyRoomMessage,
    UserProfile, UserFollow, CommunityNotification, ActivityFeed
)

@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'views', 'is_pinned', 'created_at')
    list_filter = ('category', 'is_pinned', 'is_closed', 'created_at')
    search_fields = ('title', 'author__username')
    readonly_fields = ('views', 'like_count', 'comment_count')


@admin.register(ForumPostComment)
class ForumPostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__title', 'author__username')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'views', 'is_answered', 'created_at')
    list_filter = ('is_answered', 'is_closed', 'created_at')
    search_fields = ('title', 'author__username', 'tags')
    readonly_fields = ('views',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'upvote_count', 'downvote_count', 'is_accepted')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('question__title', 'author__username')
    readonly_fields = ('upvote_count', 'downvote_count')


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'is_private', 'created_by', 'created_at')
    list_filter = ('is_private', 'created_at')
    search_fields = ('name', 'topic', 'created_by__username')


@admin.register(StudyGroupMember)
class StudyGroupMemberAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'joined_at')
    list_filter = ('joined_at',)
    search_fields = ('group__name', 'user__username')


@admin.register(LiveStudyRoom)
class LiveStudyRoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'status', 'current_members', 'started_at')
    list_filter = ('status', 'started_at')
    search_fields = ('title', 'creator__username')
    readonly_fields = ('current_members',)


@admin.register(LiveStudyRoomMember)
class LiveStudyRoomMemberAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'joined_at', 'left_at')
    list_filter = ('joined_at',)
    search_fields = ('room__title', 'user__username')


@admin.register(CommunityNotification)
class CommunityNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title')
