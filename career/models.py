from django.db import models
from authentication.models import CustomUser

# ============ INTERNSHIP & JOB POSTINGS ============

class Internship(models.Model):
    """Internship listings"""
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    
    # Details
    stipend = models.CharField(max_length=100, blank=True)  # e.g., "500-1000/month"
    duration = models.CharField(max_length=100)  # e.g., "2 months"
    location = models.CharField(max_length=255, blank=True)
    
    # Links
    apply_link = models.URLField()
    
    # Dates
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    start_date = models.DateField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    applications = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-posted_date']
    
    def __str__(self):
        return f"{self.title} - {self.company}"


class JobPosting(models.Model):
    """Job postings for placement"""
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    
    # Details
    package = models.CharField(max_length=100)  # e.g., "10-12 LPA"
    location = models.CharField(max_length=255)
    role_type = models.CharField(max_length=100)  # e.g., "Full-time", "Contract"
    
    # Requirements
    min_cgpa = models.FloatField(default=6.0)
    backlogs_allowed = models.BooleanField(default=True)
    eligible_branches = models.CharField(max_length=500, help_text="Comma-separated branches")
    
    # Links
    apply_link = models.URLField()
    
    # Dates
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    
    # Status
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    applications = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-posted_date']
    
    def __str__(self):
        return f"{self.title} - {self.company}"


class JobAlert(models.Model):
    """Job alerts for users"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_alerts')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'job']


# ============ PLACEMENT PREPARATION ============

class PlacementMaterial(models.Model):
    """Company-specific placement preparation material"""
    company = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='placement_materials/')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company} - {self.title}"


class PreviousPlacementPaper(models.Model):
    """Previous year placement papers"""
    company = models.CharField(max_length=255)
    year = models.IntegerField()
    title = models.CharField(max_length=255)
    paper_type = models.CharField(max_length=50)  # Online Assessment, Technical, HR
    file = models.FileField(upload_to='placement_papers/')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-year', '-uploaded_at']
        unique_together = ['company', 'year', 'paper_type']
    
    def __str__(self):
        return f"{self.company} - {self.year} ({self.paper_type})"


class InterviewQuestion(models.Model):
    """Interview questions database"""
    QUESTION_TYPE = [
        ('technical', 'Technical'),
        ('hr', 'HR'),
        ('behavioral', 'Behavioral'),
    ]
    
    company = models.CharField(max_length=255)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE)
    
    suggested_answer = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, default='medium')
    
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    views = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company} - {self.question_text[:50]}"


class InterviewExperience(models.Model):
    """Share interview experiences"""
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interview_experiences')
    experience_text = models.TextField()
    
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    got_offer = models.BooleanField(default=False)
    
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']


# ============ APTITUDE PRACTICE ============

class AptitudeCategory(models.Model):
    """Categories for aptitude practice"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Aptitude Categories"
    
    def __str__(self):
        return self.name


class AptitudeQuestion(models.Model):
    """Aptitude practice questions"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    category = models.ForeignKey(AptitudeCategory, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    
    # Options
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    
    # Answer
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    explanation = models.TextField(blank=True)
    
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.category.name} - Question"


class AptitudePracticeSession(models.Model):
    """User's aptitude practice sessions"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='aptitude_sessions')
    category = models.ForeignKey(AptitudeCategory, on_delete=models.CASCADE)
    
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
    skipped = models.IntegerField(default=0)
    
    time_taken = models.IntegerField(default=0)  # in seconds
    score_percentage = models.FloatField(default=0.0)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']


# ============ CODING PRACTICE ============

class CodingCategory(models.Model):
    """Categories for coding problems"""
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Coding Categories"
    
    def __str__(self):
        return self.name


class CodingProblem(models.Model):
    """Coding practice problems"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    category = models.ForeignKey(CodingCategory, on_delete=models.CASCADE, related_name='problems')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    examples = models.TextField(help_text="Problem examples and test cases")
    constraints = models.TextField(blank=True)
    
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    acceptance_rate = models.FloatField(default=0.0)
    
    attempts = models.IntegerField(default=0)
    solved_by = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class CodingSubmission(models.Model):
    """Submissions for coding problems"""
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('wrong_answer', 'Wrong Answer'),
        ('time_limit_exceeded', 'Time Limit Exceeded'),
        ('runtime_error', 'Runtime Error'),
        ('compilation_error', 'Compilation Error'),
    ]
    
    problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='coding_submissions')
    
    code = models.TextField()
    language = models.CharField(max_length=50)  # Python, Java, C++, etc.
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    execution_time = models.FloatField(null=True, blank=True)  # in ms
    memory_used = models.FloatField(null=True, blank=True)  # in MB
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']


class CodingPracticeStats(models.Model):
    """Track user's coding practice statistics"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='coding_stats')
    
    problems_solved = models.IntegerField(default=0)
    problems_attempted = models.IntegerField(default=0)
    total_submissions = models.IntegerField(default=0)
    
    easy_solved = models.IntegerField(default=0)
    medium_solved = models.IntegerField(default=0)
    hard_solved = models.IntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Coding Stats"


# ============ RESUME BUILDER ============

class ResumeTemplate(models.Model):
    """Resume templates"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='resume_templates/', blank=True)
    is_premium = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Resume(models.Model):
    """User resumes"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='resumes')
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=255, default="My Resume")
    
    # Sections
    professional_summary = models.TextField(blank=True)
    
    # Downloads
    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    
    is_default = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ResumeExperience(models.Model):
    """Work experience for resume"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_currently_working = models.BooleanField(default=False)
    
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']


class ResumeEducation(models.Model):
    """Education details for resume"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    grade = models.CharField(max_length=10, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-end_date']


class ResumeSkill(models.Model):
    """Skills for resume"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    
    skill_name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ])
    
    class Meta:
        ordering = ['skill_name']


# ============ MOCK INTERVIEW ============

class MockInterview(models.Model):
    """Mock interview sessions"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mock_interviews')
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Interview Details
    interview_type = models.CharField(max_length=50, choices=[
        ('technical', 'Technical'),
        ('hr', 'HR'),
        ('mixed', 'Mixed'),
        ('ai_generated', 'AI Generated'),
    ])
    
    total_questions = models.IntegerField(default=10)
    time_limit = models.IntegerField(default=60)  # in minutes
    
    # Results
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class MockInterviewQuestion(models.Model):
    """Questions in a mock interview"""
    interview = models.ForeignKey(MockInterview, on_delete=models.CASCADE, related_name='questions')
    
    question_text = models.TextField()
    question_order = models.IntegerField()
    
    user_answer = models.TextField(blank=True)
    is_answered = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    class Meta:
        ordering = ['question_order']


# ============ COMPANY-WISE QUESTIONS ============

class Company(models.Model):
    """Companies for interview preparation"""
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Companies"
    
    def __str__(self):
        return self.name


class CompanyQuestion(models.Model):
    """Questions specific to a company"""
    QUESTION_TYPE = [
        ('oa', 'Online Assessment'),
        ('technical', 'Technical'),
        ('hr', 'HR'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='questions')
    
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE)
    
    suggested_answer = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, default='medium')
    
    views = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company.name} - {self.question_text[:50]}"


class CompanyExperience(models.Model):
    """Interview experiences specific to company"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='experiences')
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    
    experience_text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    got_offer = models.BooleanField(default=False)
    
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
