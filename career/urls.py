from django.urls import path
from . import views

app_name = 'career'

urlpatterns = [
    # Internships
    path('internships/', views.internships_list, name='internships_list'),
    path('internships/<int:pk>/', views.internship_detail, name='internship_detail'),
    
    # Jobs
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    
    # Placement Preparation
    path('placement/materials/', views.placement_materials, name='placement_materials'),
    path('placement/papers/', views.placement_papers, name='placement_papers'),
    path('placement/papers/<int:pk>/', views.placement_paper_detail, name='placement_paper_detail'),
    path('placement/interview-questions/', views.interview_questions, name='interview_questions'),
    path('placement/experiences/', views.interview_experiences, name='interview_experiences'),
    
    # Aptitude
    path('aptitude/', views.aptitude_categories, name='aptitude_categories'),
    path('aptitude/category/<int:category_id>/', views.aptitude_practice, name='aptitude_practice'),
    path('aptitude/session/<int:session_id>/result/', views.aptitude_result, name='aptitude_result'),
    
    # Coding
    path('coding/', views.coding_problems, name='coding_problems'),
    path('coding/problem/<int:pk>/', views.coding_problem_detail, name='coding_problem_detail'),
    path('coding/submit/', views.submit_code, name='submit_code'),
    path('coding/stats/', views.coding_stats, name='coding_stats'),
    
    # Resume
    path('resume/', views.resume_list, name='resume_list'),
    path('resume/create/', views.create_resume, name='create_resume'),
    path('resume/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('resume/<int:pk>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:pk>/download/', views.download_resume, name='download_resume'),
    path('resume/templates/', views.resume_templates, name='resume_templates'),
    
    # Mock Interview
    path('mock-interview/', views.mock_interviews, name='mock_interviews'),
    path('mock-interview/start/', views.start_mock_interview, name='start_mock_interview'),
    path('mock-interview/<int:pk>/', views.mock_interview_detail, name='mock_interview_detail'),
    path('mock-interview/<int:pk>/result/', views.mock_interview_result, name='mock_interview_result'),
    
    # Company-wise Questions
    path('companies/', views.companies_list, name='companies_list'),
    path('companies/<int:company_id>/', views.company_detail, name='company_detail'),
    path('companies/<int:company_id>/questions/', views.company_questions, name='company_questions'),
    path('companies/<int:company_id>/experiences/', views.company_experiences, name='company_experiences'),
]
