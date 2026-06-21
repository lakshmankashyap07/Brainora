from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'brainora_project.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('auth/', include('authentication.urls')),
    path('courses/', include('courses.urls')),
    path('resources/', include('resources.urls')),
    path('activities/', include('activities.urls')),
    path('papers/', include('papers.urls')),
    path('academic/', include('academic.urls')),
    path('community/', include('community.urls')),
    path('career/', include('career.urls')),
    path('college/', include('college.urls')),
    path('api/', include('api.urls')),
]

# Serve media and static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
