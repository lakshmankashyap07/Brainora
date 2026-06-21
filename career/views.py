from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.decorators.http import require_http_methods
from datetime import datetime
from .models import (
    Internship, JobPosting, JobAlert,
    PlacementMaterial, PreviousPlacementPaper, InterviewQuestion, InterviewExperience,
    AptitudeCategory, AptitudeQuestion, AptitudePracticeSession,
    CodingCategory, CodingProblem, CodingSubmission, CodingPracticeStats,
    ResumeTemplate, Resume, ResumeExperience, ResumeEducation, ResumeSkill,
    MockInterview, MockInterviewQuestion,
    Company, CompanyQuestion, CompanyExperience
)

# ============ INTERNSHIPS & JOBS ============

def internships_list(request):
    """List all active internships"""
    internships = Internship.objects.filter(is_active=True)
    
    search_query = request.GET.get('q', '')
    if search_query:
        internships = internships.filter(
            Q(title__icontains=search_query) | Q(company__icontains=search_query)
        )
    
    company = request.GET.get('company', '')
    if company:
        internships = internships.filter(company__icontains=company)
    
    paginator = Paginator(internships, 10)
    page = request.GET.get('page', 1)
    internships_page = paginator.get_page(page)
    
    context = {
        'internships': internships_page,
        'search_query': search_query,
    }
    return render(request, 'career/internships_list.html', context)


def internship_detail(request, pk):
    """View internship details"""
    internship = get_object_or_404(Internship, pk=pk)
    internship.views += 1
    internship.save()
    
    context = {'internship': internship}
    return render(request, 'career/internship_detail.html', context)


def jobs_list(request):
    """List all active job postings"""
    jobs = JobPosting.objects.filter(is_active=True)
    
    search_query = request.GET.get('q', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) | Q(company__icontains=search_query)
        )
    
    package = request.GET.get('package')
    location = request.GET.get('location', '')
    
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    paginator = Paginator(jobs, 10)
    page = request.GET.get('page', 1)
    jobs_page = paginator.get_page(page)
    
    context = {
        'jobs': jobs_page,
        'search_query': search_query,
    }
    return render(request, 'career/jobs_list.html', context)


def job_detail(request, pk):
    """View job posting details"""
    job = get_object_or_404(JobPosting, pk=pk)
    job.views += 1
    job.save()
    
    context = {'job': job}
    return render(request, 'career/job_detail.html', context)


# ============ PLACEMENT PREPARATION ============

def placement_materials(request):
    """List placement preparation materials"""
    materials = PlacementMaterial.objects.all()
    
    company = request.GET.get('company', '')
    if company:
        materials = materials.filter(company__icontains=company)
    
    paginator = Paginator(materials, 12)
    page = request.GET.get('page', 1)
    materials_page = paginator.get_page(page)
    
    context = {'materials': materials_page}
    return render(request, 'career/placement_materials.html', context)


def placement_papers(request):
    """List previous placement papers"""
    papers = PreviousPlacementPaper.objects.all()
    
    company = request.GET.get('company', '')
    if company:
        papers = papers.filter(company__icontains=company)
    
    year = request.GET.get('year')
    if year:
        papers = papers.filter(year=year)
    
    paginator = Paginator(papers, 10)
    page = request.GET.get('page', 1)
    papers_page = paginator.get_page(page)
    
    context = {'papers': papers_page}
    return render(request, 'career/placement_papers.html', context)


def placement_paper_detail(request, pk):
    """View placement paper"""
    paper = get_object_or_404(PreviousPlacementPaper, pk=pk)
    paper.views += 1
    paper.save()
    
    context = {'paper': paper}
    return render(request, 'career/placement_paper_detail.html', context)


def interview_questions(request):
    """List interview questions"""
    questions = InterviewQuestion.objects.all()
    
    company = request.GET.get('company', '')
    if company:
        questions = questions.filter(company__icontains=company)
    
    q_type = request.GET.get('type')
    if q_type:
        questions = questions.filter(question_type=q_type)
    
    paginator = Paginator(questions, 15)
    page = request.GET.get('page', 1)
    questions_page = paginator.get_page(page)
    
    context = {'questions': questions_page}
    return render(request, 'career/interview_questions.html', context)


def interview_experiences(request):
    """List interview experiences"""
    experiences = InterviewExperience.objects.select_related('author')
    
    company = request.GET.get('company', '')
    if company:
        experiences = experiences.filter(company__icontains=company)
    
    paginator = Paginator(experiences, 10)
    page = request.GET.get('page', 1)
    experiences_page = paginator.get_page(page)
    
    context = {'experiences': experiences_page}
    return render(request, 'career/interview_experiences.html', context)


# ============ APTITUDE PRACTICE ============

def aptitude_categories(request):
    """List aptitude categories"""
    categories = AptitudeCategory.objects.all()
    
    context = {'categories': categories}
    return render(request, 'career/aptitude_categories.html', context)


def aptitude_practice(request, category_id):
    """Practice aptitude questions"""
    category = get_object_or_404(AptitudeCategory, pk=category_id)
    questions = category.questions.all()
    
    difficulty = request.GET.get('difficulty')
    if difficulty:
        questions = questions.filter(difficulty=difficulty)
    
    paginator = Paginator(questions, 10)
    page = request.GET.get('page', 1)
    questions_page = paginator.get_page(page)
    
    context = {
        'category': category,
        'questions': questions_page,
    }
    return render(request, 'career/aptitude_practice.html', context)


def aptitude_result(request, session_id):
    """View aptitude practice result"""
    session = get_object_or_404(AptitudePracticeSession, pk=session_id)
    
    if session.user != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    context = {'session': session}
    return render(request, 'career/aptitude_result.html', context)


# ============ CODING PRACTICE ============

def coding_problems(request):
    """List coding problems"""
    problems = CodingProblem.objects.all()
    
    category = request.GET.get('category')
    if category:
        problems = problems.filter(category_id=category)
    
    difficulty = request.GET.get('difficulty')
    if difficulty:
        problems = problems.filter(difficulty=difficulty)
    
    paginator = Paginator(problems, 12)
    page = request.GET.get('page', 1)
    problems_page = paginator.get_page(page)
    
    categories = CodingCategory.objects.all()
    
    context = {
        'problems': problems_page,
        'categories': categories,
    }
    return render(request, 'career/coding_problems.html', context)


def coding_problem_detail(request, pk):
    """View coding problem details"""
    problem = get_object_or_404(CodingProblem, pk=pk)
    
    submissions = problem.submissions.all()
    user_submissions = []
    if request.user.is_authenticated:
        user_submissions = submissions.filter(user=request.user)
    
    context = {
        'problem': problem,
        'user_submissions': user_submissions,
    }
    return render(request, 'career/coding_problem_detail.html', context)


@login_required
def submit_code(request):
    """Submit code for a problem"""
    if request.method == 'POST':
        problem_id = request.POST.get('problem_id')
        code = request.POST.get('code')
        language = request.POST.get('language')
        
        problem = get_object_or_404(CodingProblem, pk=problem_id)
        
        submission = CodingSubmission.objects.create(
            problem=problem,
            user=request.user,
            code=code,
            language=language,
            status='accepted'  # In real scenario, run on sandbox
        )
        
        return JsonResponse({'success': True, 'submission_id': submission.id})
    
    return JsonResponse({'success': False})


@login_required
def coding_stats(request):
    """View user coding statistics"""
    stats, _ = CodingPracticeStats.objects.get_or_create(user=request.user)
    
    context = {'stats': stats}
    return render(request, 'career/coding_stats.html', context)


# ============ RESUME BUILDER ============

def resume_list(request):
    """List resumes"""
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    resumes = request.user.resumes.all()
    templates = ResumeTemplate.objects.all()
    
    context = {
        'resumes': resumes,
        'templates': templates,
    }
    return render(request, 'career/resume_list.html', context)


@login_required
def create_resume(request):
    """Create new resume"""
    if request.method == 'POST':
        title = request.POST.get('title', 'My Resume')
        template_id = request.POST.get('template')
        
        template = None
        if template_id:
            template = get_object_or_404(ResumeTemplate, pk=template_id)
        
        resume = Resume.objects.create(
            user=request.user,
            title=title,
            template=template
        )
        
        return redirect('career:resume_detail', pk=resume.pk)
    
    templates = ResumeTemplate.objects.all()
    context = {'templates': templates}
    return render(request, 'career/create_resume.html', context)


def resume_detail(request, pk):
    """View resume"""
    resume = get_object_or_404(Resume, pk=pk)
    
    if resume.user != request.user and not request.user.is_staff and not resume.is_public:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    resume.views += 1
    resume.save()
    
    experiences = resume.experiences.all()
    educations = resume.educations.all()
    skills = resume.skills.all()
    
    context = {
        'resume': resume,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
    }
    return render(request, 'career/resume_detail.html', context)


@login_required
def edit_resume(request, pk):
    """Edit resume"""
    resume = get_object_or_404(Resume, pk=pk)
    
    if resume.user != request.user:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        resume.title = request.POST.get('title', resume.title)
        resume.professional_summary = request.POST.get('summary', '')
        resume.save()
        return redirect('career:resume_detail', pk=resume.pk)
    
    context = {'resume': resume}
    return render(request, 'career/edit_resume.html', context)


@login_required
def download_resume(request, pk):
    """Download resume as PDF"""
    resume = get_object_or_404(Resume, pk=pk)
    
    if resume.user != request.user and not request.user.is_staff and not resume.is_public:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    resume.downloads += 1
    resume.save()
    
    # In real scenario, generate PDF using reportlab or weasyprint
    return JsonResponse({'success': True, 'message': 'Resume download initiated'})


def resume_templates(request):
    """List resume templates"""
    templates = ResumeTemplate.objects.all()
    
    paginator = Paginator(templates, 12)
    page = request.GET.get('page', 1)
    templates_page = paginator.get_page(page)
    
    context = {'templates': templates_page}
    return render(request, 'career/resume_templates.html', context)


# ============ MOCK INTERVIEW ============

def mock_interviews(request):
    """List mock interviews"""
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    interviews = request.user.mock_interviews.all()
    
    context = {'interviews': interviews}
    return render(request, 'career/mock_interviews.html', context)


@login_required
def start_mock_interview(request):
    """Start a new mock interview"""
    if request.method == 'POST':
        interview_type = request.POST.get('type', 'technical')
        
        interview = MockInterview.objects.create(
            user=request.user,
            title=f'Mock Interview - {interview_type.title()}',
            interview_type=interview_type
        )
        
        # Generate questions (in real scenario, fetch from DB or AI)
        for i in range(interview.total_questions):
            MockInterviewQuestion.objects.create(
                interview=interview,
                question_text=f'Sample Question {i+1}',
                question_order=i+1
            )
        
        return redirect('career:mock_interview_detail', pk=interview.pk)
    
    context = {'interview_types': ['technical', 'hr', 'mixed', 'ai_generated']}
    return render(request, 'career/start_mock_interview.html', context)


def mock_interview_detail(request, pk):
    """View mock interview questions"""
    interview = get_object_or_404(MockInterview, pk=pk)
    
    if interview.user != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    questions = interview.questions.all()
    
    context = {
        'interview': interview,
        'questions': questions,
    }
    return render(request, 'career/mock_interview_detail.html', context)


def mock_interview_result(request, pk):
    """View mock interview results"""
    interview = get_object_or_404(MockInterview, pk=pk)
    
    if interview.user != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    context = {'interview': interview}
    return render(request, 'career/mock_interview_result.html', context)


# ============ COMPANIES ============

def companies_list(request):
    """List all companies"""
    companies = Company.objects.all()
    
    search_query = request.GET.get('q', '')
    if search_query:
        companies = companies.filter(name__icontains=search_query)
    
    paginator = Paginator(companies, 20)
    page = request.GET.get('page', 1)
    companies_page = paginator.get_page(page)
    
    context = {
        'companies': companies_page,
        'search_query': search_query,
    }
    return render(request, 'career/companies_list.html', context)


def company_detail(request, company_id):
    """View company details"""
    company = get_object_or_404(Company, pk=company_id)
    
    context = {'company': company}
    return render(request, 'career/company_detail.html', context)


def company_questions(request, company_id):
    """View company-specific questions"""
    company = get_object_or_404(Company, pk=company_id)
    questions = company.questions.all()
    
    q_type = request.GET.get('type')
    if q_type:
        questions = questions.filter(question_type=q_type)
    
    paginator = Paginator(questions, 15)
    page = request.GET.get('page', 1)
    questions_page = paginator.get_page(page)
    
    context = {
        'company': company,
        'questions': questions_page,
    }
    return render(request, 'career/company_questions.html', context)


def company_experiences(request, company_id):
    """View company interview experiences"""
    company = get_object_or_404(Company, pk=company_id)
    experiences = company.experiences.all()
    
    paginator = Paginator(experiences, 10)
    page = request.GET.get('page', 1)
    experiences_page = paginator.get_page(page)
    
    context = {
        'company': company,
        'experiences': experiences_page,
    }
    return render(request, 'career/company_experiences.html', context)
