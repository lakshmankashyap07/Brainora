from django.urls import path
from . import views

urlpatterns = [
    # Root: show login (dashboard is protected)
    path('', views.login_view, name='home'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('upload_resource/', views.upload_resource_view, name='upload_resource'),
    
    # Courses
    path('courses/', views.courses_view, name='courses'),
    path('course/<int:course_id>/', views.course_detail_view, name='course_detail'),
    
    # Previous Year Papers
    path('papers/', views.papers_view, name='papers'),
    
    # College Activities
    path('activities/', views.activities_view, name='activities'),
]
