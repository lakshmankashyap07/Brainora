from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # Forum
    path('forum/', views.forum_list, name='forum_list'),
    path('forum/category/<int:category_id>/', views.forum_category, name='forum_category'),
    path('forum/post/create/', views.create_post, name='create_post'),
    path('forum/post/<int:pk>/', views.post_detail, name='post_detail'),
    path('forum/post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('forum/post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('forum/post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('forum/post/<int:pk>/like/', views.like_post, name='like_post'),
    
    # Q&A
    path('qa/', views.questions_list, name='questions_list'),
    path('qa/ask/', views.ask_question, name='ask_question'),
    path('qa/question/<int:pk>/', views.question_detail, name='question_detail'),
    path('qa/question/<int:pk>/answer/', views.answer_question, name='answer_question'),
    path('qa/answer/<int:pk>/vote/', views.vote_answer, name='vote_answer'),
    path('qa/answer/<int:pk>/accept/', views.accept_answer, name='accept_answer'),
    
    # Study Groups
    path('study-groups/', views.study_groups_list, name='study_groups_list'),
    path('study-groups/create/', views.create_study_group, name='create_study_group'),
    path('study-groups/<int:pk>/', views.study_group_detail, name='study_group_detail'),
    path('study-groups/<int:pk>/join/', views.join_study_group, name='join_study_group'),
    path('study-groups/<int:pk>/leave/', views.leave_study_group, name='leave_study_group'),
    
    # Live Study Rooms
    path('live-rooms/', views.live_rooms_list, name='live_rooms_list'),
    path('live-rooms/create/', views.create_live_room, name='create_live_room'),
    path('live-rooms/<int:pk>/', views.live_room_detail, name='live_room_detail'),
    path('live-rooms/<int:pk>/join/', views.join_live_room, name='join_live_room'),
    path('live-rooms/<int:pk>/leave/', views.leave_live_room, name='leave_live_room'),
    
    # User Profiles
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('profile/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    
    # Notifications
    path('notifications/', views.notifications_list, name='notifications_list'),
]
