from django.urls import path
from . import views

app_name = 'academic'

urlpatterns = [
    # Resource Management
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/upload/', views.upload_resource, name='upload_resource'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('resources/<int:pk>/download/', views.download_resource, name='download_resource'),
    path('resources/<int:pk>/bookmark/', views.bookmark_resource, name='bookmark_resource'),
    path('resources/<int:pk>/like/', views.like_resource, name='like_resource'),
    path('resources/<int:pk>/report/', views.report_resource, name='report_resource'),
    path('resources/<int:pk>/edit/', views.edit_resource, name='edit_resource'),
    path('resources/<int:pk>/delete/', views.delete_resource, name='delete_resource'),
    
    # Syllabus
    path('syllabus/', views.syllabus_list, name='syllabus_list'),
    path('syllabus/<int:pk>/', views.syllabus_detail, name='syllabus_detail'),
    
    # Academic Calendar
    path('calendar/', views.calendar_view, name='calendar'),
    
    # TimeTable
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/<int:semester>/', views.timetable_semester, name='timetable_semester'),
]
