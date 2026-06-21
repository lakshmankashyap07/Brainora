from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    CourseViewSet,
    ResourceViewSet,
    PreviousYearPaperViewSet,
    CollegeActivityViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'papers', PreviousYearPaperViewSet, basename='paper')
router.register(r'activities', CollegeActivityViewSet, basename='activity')

urlpatterns = [
    # JWT Auth Endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Router API Endpoints
    path('', include(router.urls)),
]
