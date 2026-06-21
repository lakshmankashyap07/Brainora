from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list_view, name='list'),
    path('<int:pk>/', views.course_detail_view, name='detail'),
]
