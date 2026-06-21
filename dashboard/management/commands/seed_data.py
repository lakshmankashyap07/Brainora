import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from courses.models import Course
from resources.models import Resource
from papers.models import PreviousYearPaper
from activities.models import CollegeActivity

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the Brainora database with initial sample data (DISABLED by default)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Allow creation of sample data and default admin account',
        )

    def handle(self, *args, **kwargs):
        force = bool(kwargs.get('force'))
        if not force:
            self.stdout.write(
                self.style.WARNING(
                    'seed_data is disabled by default. Re-run with: python manage.py seed_data --force'
                )
            )
            return

        self.stdout.write("Seeding Brainora database (force enabled)...")

        # 1. Create Superuser if not exists
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser(
                username="admin",
                email="admin@brainora.com",
                password="adminpassword123",
                full_name="Brainora Admin",
                role="Admin",
                is_verified=True,
                college="IIT Delhi",
                university="Delhi University"
            )
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created (pass: adminpassword123)"))
        else:
            admin_user = User.objects.get(username="admin")


        # 2. Create Sample Students
        students_data = [
            {"username": "john_doe", "email": "john@college.edu", "name": "John Doe", "branch": "Computer Science", "sem": 3},
            {"username": "jane_smith", "email": "jane@college.edu", "name": "Jane Smith", "branch": "Information Technology", "sem": 2},
        ]
        students = []
        for s in students_data:
            user, created = User.objects.get_or_create(
                username=s['username'],
                defaults={
                    "email": s['email'],
                    "full_name": s['name'],
                    "role": "Student",
                    "is_verified": True,
                    "college": "IIT Delhi",
                    "university": "Delhi University",
                    "branch": s['branch'],
                    "semester": s['sem']
                }
            )
            if created:
                user.set_password("studentpassword123")
                user.save()
                self.stdout.write(f"Student user '{user.username}' created.")
            students.append(user)

        # 3. Create Sample Instructors
        instructors_data = [
            {"username": "prof_albert", "email": "albert@college.edu", "name": "Prof. Albert Einstein"},
            {"username": "prof_curie", "email": "curie@college.edu", "name": "Prof. Marie Curie"},
        ]
        instructors = []
        for ins in instructors_data:
            user, created = User.objects.get_or_create(
                username=ins['username'],
                defaults={
                    "email": ins['email'],
                    "full_name": ins['name'],
                    "role": "Instructor",
                    "is_verified": True,
                    "college": "IIT Delhi",
                    "university": "Delhi University"
                }
            )
            if created:
                user.set_password("profpassword123")
                user.save()
                self.stdout.write(f"Instructor user '{user.username}' created.")
            instructors.append(user)

        # 4. Create Sample Courses
        courses_data = [
            {"code": "CS101", "title": "Introduction to Computer Science", "sem": 1, "credits": 3, "ins": instructors[0]},
            {"code": "CS102", "title": "Data Structures & Algorithms", "sem": 2, "credits": 4, "ins": instructors[0]},
            {"code": "CS303", "title": "Database Management Systems", "sem": 3, "credits": 3, "ins": instructors[1]},
            {"code": "CS404", "title": "Operating Systems", "sem": 4, "credits": 4, "ins": instructors[1]},
        ]
        courses = []
        for c in courses_data:
            course, created = Course.objects.get_or_create(
                course_code=c['code'],
                defaults={
                    "title": c['title'],
                    "semester": c['sem'],
                    "credits": c['credits'],
                    "instructor": c['ins'].full_name
                }
            )
            if created:
                self.stdout.write(f"Course '{course.course_code}' created.")
            courses.append(course)

        # 5. Create Sample Resources
        resources_data = [
            {
                "title": "CS101 Lecture Notes - Week 1-4",
                "category": "Notes",
                "desc": "Introduction to programming concepts, variables, control flow and functions.",
                "link": "https://drive.google.com/file/d/sample-notes-key/view",
                "user": instructors[0]
            },
            {
                "title": "Data Structures Assignment 1 - Binary Trees",
                "category": "Assignments",
                "desc": "Binary tree operations, traversals and depth questions with sample answers.",
                "link": "https://drive.google.com/file/d/sample-assignment/view",
                "user": students[0]
            },
            {
                "title": "DBMS Lab 2 - SQL Query Guidelines",
                "category": "Lab Files",
                "desc": "SQL DDL and DML queries sheet containing table joins and aggregate functions.",
                "link": "https://drive.google.com/file/d/sample-lab-sheet/view",
                "user": students[1]
            },
            {
                "title": "Complete Software Engineer Roadmap 2026",
                "category": "Roadmaps",
                "desc": "Comprehensive step-by-step roadmap from foundations to system designs and clouds.",
                "link": "https://roadmap.sh/computer-science",
                "user": students[0]
            },
            {
                "title": "IIT Delhi Computer Science Study Telegram Group",
                "category": "Telegram Groups",
                "desc": "Join this peer network group to resolve doubts, share notes and talk syllabus.",
                "link": "https://t.me/iitd_cs_study_group",
                "user": students[0]
            },
            {
                "title": "CS102 Holiday Homework - Array Operations",
                "category": "Holiday Homework",
                "desc": "Holiday homework packet detailing custom sorting algorithms and time complexity graphs.",
                "link": "https://drive.google.com/file/d/sample-holiday/view",
                "user": instructors[0]
            }
        ]
        for res in resources_data:
            resource, created = Resource.objects.get_or_create(
                title=res['title'],
                defaults={
                    "category": res['category'],
                    "description": res['desc'],
                    "external_link": res['link'],
                    "uploaded_by": res['user'],
                    "downloads": 12
                }
            )
            if created:
                # Add default likes and bookmarks
                resource.likes.add(students[0])
                resource.bookmarks.add(students[1])
                self.stdout.write(f"Resource '{resource.title}' created.")

        # 6. Create Sample Previous Year Papers
        papers_data = [
            {
                "course": courses[0],
                "title": "CS101 Midterm Examination 2023",
                "type": "Midterm",
                "year": 2023,
                "user": instructors[0]
            },
            {
                "course": courses[1],
                "title": "CS102 Final Term Theory Paper 2022",
                "type": "Final",
                "year": 2022,
                "user": instructors[0]
            },
            {
                "course": courses[2],
                "title": "CS303 Quiz 1 - Normal Forms",
                "type": "Quiz",
                "year": 2023,
                "user": instructors[1]
            }
        ]
        for p in papers_data:
            # Note: since pdf_file is a FileField, we'll assign a placeholder file name
            # in code, which is fine since we serve downloads via external links or local fallback
            paper, created = PreviousYearPaper.objects.get_or_create(
                title=p['title'],
                defaults={
                    "course": p['course'],
                    "paper_type": p['type'],
                    "year": p['year'],
                    "pdf_file": "papers/placeholder.pdf",
                    "uploaded_by": p['user']
                }
            )
            if created:
                self.stdout.write(f"PYP '{paper.title}' created.")

        # 7. Create Sample College Activities
        activities_data = [
            {
                "title": "Annual Coding Hackathon 2026",
                "type": "Event",
                "desc": "A 24-hour campus hackathon organized by the Coding Society. Prize pool of 100k!",
                "date": timezone.now().date() + timedelta(days=2),
                "loc": "CS Seminar Hall 2",
                "user": admin_user
            },
            {
                "title": "Term Project Submission Deadline",
                "type": "Deadline",
                "desc": "DBMS term project schemas and database designs must be submitted by tonight.",
                "date": timezone.now().date() + timedelta(days=1),
                "loc": "Online Submission Portal",
                "user": instructors[1]
            },
            {
                "title": "Semester Registration Notification",
                "type": "Announcement",
                "desc": "Odd semester registrations will open next Monday. Complete payments on student port.",
                "date": timezone.now().date() + timedelta(days=5),
                "loc": "Administrative Building",
                "user": admin_user
            },
            {
                "title": "Monsoon Festival Holidays Circular",
                "type": "Holiday",
                "desc": "The college will remain closed next Friday in observance of Monsoon Festival.",
                "date": timezone.now().date() + timedelta(days=7),
                "loc": "Campus Wide",
                "user": admin_user
            }
        ]
        for act in activities_data:
            activity, created = CollegeActivity.objects.get_or_create(
                title=act['title'],
                defaults={
                    "activity_type": act['type'],
                    "description": act['desc'],
                    "activity_date": act['date'],
                    "location": act['loc'],
                    "created_by": act['user']
                }
            )
            if created:
                self.stdout.write(f"Activity '{activity.title}' created.")
                
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
