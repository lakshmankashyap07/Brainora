from django.urls import path
from . import views

app_name = 'college'

urlpatterns = [
    # Announcements
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcements/<int:pk>/like/', views.announcement_like, name='announcement_like'),
    path('announcements/<int:pk>/comment/', views.announcement_comment, name='announcement_comment'),
    
    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/register/', views.event_register, name='event_register'),
    path('events/<int:pk>/unregister/', views.event_unregister, name='event_unregister'),
    
    # Clubs
    path('clubs/', views.club_list, name='club_list'),
    path('clubs/<slug:slug>/', views.club_detail, name='club_detail'),
    path('clubs/<slug:slug>/join/', views.club_join, name='club_join'),
    path('clubs/<slug:slug>/leave/', views.club_leave, name='club_leave'),
    
    # Workshops
    path('workshops/', views.workshop_list, name='workshop_list'),
    path('workshops/<int:pk>/', views.workshop_detail, name='workshop_detail'),
    path('workshops/<int:pk>/register/', views.workshop_register, name='workshop_register'),
    path('workshops/<int:pk>/feedback/', views.workshop_feedback, name='workshop_feedback'),
    
    # Lost & Found
    path('lost-found/', views.lost_found_list, name='lost_found_list'),
    path('lost-found/create/', views.lost_found_create, name='lost_found_create'),
    path('lost-found/<int:pk>/', views.lost_found_detail, name='lost_found_detail'),
    
    # Complaints
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/create/', views.complaint_create, name='complaint_create'),
    path('complaints/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    
    # Faculty
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
    
    # Campus Map
    path('map/', views.campus_map, name='campus_map'),
    path('map/<slug:slug>/', views.campus_location_detail, name='campus_location_detail'),
]
