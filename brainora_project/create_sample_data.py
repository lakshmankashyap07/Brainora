#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brainora.settings')
django.setup()

from authentication.models import CustomUser, Course, PreviousYearPaper, CollegeActivity
from datetime import datetime, timedelta

# Create sample courses
courses = [
    {
        'code': 'CS101',
        'title': 'Introduction to Computer Science',
        'semester': 1,
        'instructor': 'Dr. John Smith',
        'description': 'Fundamental concepts of computer science and programming.',
        'credits': 4
    },
    {
        'code': 'CS102',
        'title': 'Data Structures',
        'semester': 1,
        'instructor': 'Dr. Jane Doe',
        'description': 'Learn about arrays, linked lists, trees, and graphs.',
        'credits': 4
    },
    {
        'code': 'CS201',
        'title': 'Database Management Systems',
        'semester': 2,
        'instructor': 'Dr. Michael Johnson',
        'description': 'Relational databases, SQL, and normalization.',
        'credits': 3
    },
]

for course_data in courses:
    Course.objects.get_or_create(
        code=course_data['code'],
        defaults={
            'title': course_data['title'],
            'semester': course_data['semester'],
            'instructor': course_data['instructor'],
            'description': course_data['description'],
            'credits': course_data['credits'],
        }
    )

print("✓ Created sample courses")

# Create sample activities
activities = [
    {
        'title': 'Semester Exam Starts',
        'activity_type': 'deadline',
        'description': 'Final examinations for Semester 1 begin.',
        'date': datetime.now() + timedelta(days=15),
        'location': 'Main Campus'
    },
    {
        'title': 'Tech Talk: AI & Machine Learning',
        'activity_type': 'event',
        'description': 'Guest speaker from leading tech company discussing AI applications.',
        'date': datetime.now() + timedelta(days=7),
        'location': 'Auditorium Hall'
    },
    {
        'title': 'Assignment 1 Due',
        'activity_type': 'deadline',
        'description': 'Submit assignment on Data Structures. Marks: 10',
        'date': datetime.now() + timedelta(days=3),
        'location': None
    },
    {
        'title': 'Winter Holidays Declaration',
        'activity_type': 'announcement',
        'description': 'College will remain closed from Dec 20 to Jan 5.',
        'date': datetime.now(),
        'location': None
    },
]

for activity_data in activities:
    CollegeActivity.objects.get_or_create(
        title=activity_data['title'],
        defaults={
            'activity_type': activity_data['activity_type'],
            'description': activity_data['description'],
            'date': activity_data['date'],
            'location': activity_data['location'],
        }
    )

print("✓ Created sample activities")

print("\n✅ Sample data created successfully!")
print("\nNext steps:")
print("1. Create a superuser: python manage.py createsuperuser")
print("2. Run server: python manage.py runserver")
print("3. Visit: http://127.0.0.1:8000/auth/")
