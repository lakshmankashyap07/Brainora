from django.urls import path
from . import views

urlpatterns = [
    # Root: show home page
    path('', views.home_view, name='home'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('upload_resource/', views.upload_resource_view, name='upload_resource'),
    path('upload/', views.upload_page_view, name='upload_page'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    
    # Courses
    path('courses/', views.courses_view, name='courses'),
    path('course/<int:course_id>/', views.course_detail_view, name='course_detail'),
    
    # Previous Year Papers
    path('papers/', views.papers_view, name='papers'),
    
    # College Activities
    path('activities/', views.activities_view, name='activities'),
    
    # Privacy Policy
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    
    # About
    path('about/', views.about_view, name='about'),
    path('about/member/<slug:member>/', views.team_member_view, name='team_member'),
    
    # WhatsApp
    path('whatsapp/', views.whatsapp_view, name='whatsapp'),
    
    # Telegram Premium (PIN protected)
    path('telegram-premium/', views.telegram_premium_view, name='telegram_premium'),
    path('telegram/', views.telegram_premium_view, name='telegram'),
    # Resources by category
    path('resources/<slug:category_slug>/', views.resource_list_view, name='resource_list'),
    
    # Delete Views
    path('paper/<int:pk>/delete/', views.delete_paper_view, name='delete_paper'),
    path('activity/<int:pk>/delete/', views.delete_activity_view, name='delete_activity'),
    path('resource/<int:pk>/delete/', views.delete_resource_view, name='delete_resource'),
]
