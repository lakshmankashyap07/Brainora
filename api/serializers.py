from rest_framework import serializers
from django.contrib.auth import get_user_model
from courses.models import Course
from resources.models import Resource
from papers.models import PreviousYearPaper
from activities.models import CollegeActivity

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'role', 'college', 'branch', 'semester', 'profile_picture']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    uploaded_by_details = UserSerializer(source='uploaded_by', read_only=True)
    likes_count = serializers.IntegerField(source='total_likes', read_only=True)
    bookmarks_count = serializers.IntegerField(source='total_bookmarks', read_only=True)

    class Meta:
        model = Resource
        fields = [
            'id', 'title', 'category', 'description', 'file', 
            'external_link', 'uploaded_by', 'uploaded_by_details', 
            'downloads', 'likes_count', 'bookmarks_count', 'created_at'
        ]
        read_only_fields = ['uploaded_by', 'downloads']

    def create(self, validated_data):
        # Automatically assign the request user as uploader
        request = self.context.get('request')
        if request and request.user:
            validated_data['uploaded_by'] = request.user
        return super().create(validated_data)


class PreviousYearPaperSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    uploaded_by_details = UserSerializer(source='uploaded_by', read_only=True)

    class Meta:
        model = PreviousYearPaper
        fields = [
            'id', 'course', 'course_details', 'title', 
            'paper_type', 'year', 'pdf_file', 'uploaded_by', 
            'uploaded_by_details', 'created_at'
        ]
        read_only_fields = ['uploaded_by']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['uploaded_by'] = request.user
        return super().create(validated_data)


class CollegeActivitySerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)

    class Meta:
        model = CollegeActivity
        fields = [
            'id', 'title', 'activity_type', 'description', 
            'activity_date', 'location', 'image', 'created_by', 
            'created_by_details', 'created_at'
        ]
        read_only_fields = ['created_by']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
        return super().create(validated_data)
