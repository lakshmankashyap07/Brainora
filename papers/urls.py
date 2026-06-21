from django.urls import path
from . import views

app_name = 'papers'

urlpatterns = [
    path('', views.paper_list_view, name='list'),
]
