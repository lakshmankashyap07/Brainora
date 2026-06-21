from django.contrib import admin
from .models import (
    Internship, JobPosting, JobAlert,
    PlacementMaterial, PreviousPlacementPaper, InterviewQuestion, InterviewExperience,
    AptitudeCategory, AptitudeQuestion, AptitudePracticeSession,
    CodingCategory, CodingProblem, CodingSubmission, CodingPracticeStats,
    ResumeTemplate, Resume, ResumeExperience, ResumeEducation, ResumeSkill,
    MockInterview, MockInterviewQuestion,
    Company, CompanyQuestion, CompanyExperience
)

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'deadline', 'is_active', 'applications')
    list_filter = ('is_active', 'deadline')
    search_fields = ('title', 'company')
    readonly_fields = ('views', 'applications')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'package', 'deadline', 'is_active')
    list_filter = ('is_active', 'deadline')
    search_fields = ('title', 'company')
    readonly_fields = ('views', 'applications')


@admin.register(PlacementMaterial)
class PlacementMaterialAdmin(admin.ModelAdmin):
    list_display = ('company', 'title', 'created_at')
    list_filter = ('company', 'created_at')
    search_fields = ('company', 'title')


@admin.register(PreviousPlacementPaper)
class PreviousPlacementPaperAdmin(admin.ModelAdmin):
    list_display = ('company', 'year', 'paper_type', 'downloads')
    list_filter = ('company', 'year', 'paper_type')
    search_fields = ('company',)
    readonly_fields = ('views', 'downloads')


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('company', 'question_type', 'difficulty', 'views')
    list_filter = ('company', 'question_type', 'difficulty')
    search_fields = ('company', 'question_text')
    readonly_fields = ('views',)


@admin.register(InterviewExperience)
class InterviewExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'author', 'rating', 'got_offer', 'created_at')
    list_filter = ('company', 'rating', 'got_offer', 'created_at')
    search_fields = ('company', 'author__username')


@admin.register(AptitudeCategory)
class AptitudeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(AptitudeQuestion)
class AptitudeQuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'difficulty', 'created_at')
    list_filter = ('category', 'difficulty')
    search_fields = ('question_text',)


@admin.register(AptitudePracticeSession)
class AptitudePracticeSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'score_percentage', 'completed_at')
    list_filter = ('category', 'completed_at')
    search_fields = ('user__username',)
    readonly_fields = ('score_percentage',)


@admin.register(CodingCategory)
class CodingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CodingProblem)
class CodingProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'solved_by')
    list_filter = ('category', 'difficulty')
    search_fields = ('title',)


@admin.register(CodingSubmission)
class CodingSubmissionAdmin(admin.ModelAdmin):
    list_display = ('problem', 'user', 'status', 'language', 'submitted_at')
    list_filter = ('status', 'language', 'submitted_at')
    search_fields = ('problem__title', 'user__username')


@admin.register(CodingPracticeStats)
class CodingPracticeStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'problems_solved', 'problems_attempted')
    search_fields = ('user__username',)


@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_premium', 'created_at')
    list_filter = ('is_premium',)
    search_fields = ('name',)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_default', 'is_public', 'updated_at')
    list_filter = ('is_default', 'is_public', 'updated_at')
    search_fields = ('user__username', 'title')


@admin.register(MockInterview)
class MockInterviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'interview_type', 'score', 'completed_at')
    list_filter = ('interview_type', 'completed_at')
    search_fields = ('user__username', 'title')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CompanyQuestion)
class CompanyQuestionAdmin(admin.ModelAdmin):
    list_display = ('company', 'question_type', 'difficulty', 'views')
    list_filter = ('company', 'question_type', 'difficulty')
    search_fields = ('company__name', 'question_text')
