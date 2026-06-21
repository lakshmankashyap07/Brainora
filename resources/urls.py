from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resource_list_view, name='list'),
    path('<int:pk>/', views.resource_detail_view, name='detail'),
    path('upload/', views.upload_resource_view, name='upload'),
    path('<int:pk>/like/', views.like_resource_view, name='like'),
    path('<int:pk>/bookmark/', views.bookmark_resource_view, name='bookmark'),
    path('<int:pk>/download/', views.download_resource_view, name='download'),
    path('<int:pk>/delete/', views.delete_resource_view, name='delete'),
]
