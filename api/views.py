from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from courses.models import Course
from resources.models import Resource
from papers.models import PreviousYearPaper
from activities.models import CollegeActivity

from .serializers import (
    CourseSerializer,
    ResourceSerializer,
    PreviousYearPaperSerializer,
    CollegeActivitySerializer,
    UserSerializer
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['course_code', 'title', 'instructor']

    def get_queryset(self):
        queryset = Course.objects.all()
        semester = self.request.query_params.get('semester')
        if semester:
            queryset = queryset.filter(semester=semester)
        return queryset


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = Resource.objects.all()
        category = self.request.query_params.get('category')
        uploaded_by = self.request.query_params.get('uploaded_by')
        if category:
            queryset = queryset.filter(category=category)
        if uploaded_by:
            queryset = queryset.filter(uploaded_by_id=uploaded_by)
        return queryset

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        resource = self.get_object()
        user = request.user
        if user in resource.likes.all():
            resource.likes.remove(user)
            return Response({'status': 'unliked', 'total_likes': resource.total_likes()})
        else:
            resource.likes.add(user)
            return Response({'status': 'liked', 'total_likes': resource.total_likes()})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def bookmark(self, request, pk=None):
        resource = self.get_object()
        user = request.user
        if user in resource.bookmarks.all():
            resource.bookmarks.remove(user)
            return Response({'status': 'unbookmarked', 'total_bookmarks': resource.total_bookmarks()})
        else:
            resource.bookmarks.add(user)
            return Response({'status': 'bookmarked', 'total_bookmarks': resource.total_bookmarks()})


class PreviousYearPaperViewSet(viewsets.ModelViewSet):
    queryset = PreviousYearPaper.objects.all()
    serializer_class = PreviousYearPaperSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        queryset = PreviousYearPaper.objects.all()
        paper_type = self.request.query_params.get('paper_type')
        course = self.request.query_params.get('course')
        year = self.request.query_params.get('year')
        if paper_type:
            queryset = queryset.filter(paper_type=paper_type)
        if course:
            queryset = queryset.filter(course_id=course)
        if year:
            queryset = queryset.filter(year=year)
        return queryset

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class CollegeActivityViewSet(viewsets.ModelViewSet):
    queryset = CollegeActivity.objects.all()
    serializer_class = CollegeActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'location']

    def get_queryset(self):
        queryset = CollegeActivity.objects.all()
        activity_type = self.request.query_params.get('activity_type')
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
