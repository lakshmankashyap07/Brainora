#!/usr/bin/env python
"""Generate stub templates for all module views"""

import os
from pathlib import Path

# Template stub - using different format string method
STUB_TEMPLATE = """{% extends 'base.html' %}
{% block title %}{title} - Brainora{% endblock %}
{% block content %}
<div class="container py-4">
    <div class="glass-panel p-5">
        <h1 class="text-gradient">{title}</h1>
        <p class="text-secondary mt-3">This template will be implemented soon.</p>
        <p class="text-secondary">View: {view_name}</p>
    </div>
</div>
{% endblock %}
"""

# List of templates to create
TEMPLATES = {
    'academic': [
        ('syllabus_list.html', 'Syllabus', 'syllabus_list'),
        ('calendar.html', 'Academic Calendar', 'calendar_view'),
        ('timetable.html', 'Time Table', 'timetable_view'),
    ],
    'community': [
        ('questions_list.html', 'Questions & Answers', 'questions_list'),
        ('ask_question.html', 'Ask Question', 'ask_question'),
        ('question_detail.html', 'Question Detail', 'question_detail'),
        ('answer_question.html', 'Answer Question', 'answer_question'),
        ('study_groups_list.html', 'Study Groups', 'study_groups_list'),
        ('create_study_group.html', 'Create Study Group', 'create_study_group'),
        ('study_group_detail.html', 'Study Group Detail', 'study_group_detail'),
        ('live_rooms_list.html', 'Live Study Rooms', 'live_rooms_list'),
        ('create_live_room.html', 'Create Live Room', 'create_live_room'),
        ('live_room_detail.html', 'Live Room Detail', 'live_room_detail'),
        ('user_profile.html', 'User Profile', 'user_profile'),
        ('notifications_list.html', 'Notifications', 'notifications_list'),
        ('post_detail.html', 'Post Detail', 'post_detail'),
        ('edit_post.html', 'Edit Post', 'edit_post'),
        ('confirm_delete.html', 'Confirm Delete', 'delete_post'),
    ],
    'career': [
        ('job_detail.html', 'Job Details', 'job_detail'),
        ('internship_detail.html', 'Internship Details', 'internship_detail'),
        ('placement_materials.html', 'Placement Materials', 'placement_materials'),
        ('placement_papers.html', 'Placement Papers', 'placement_papers'),
        ('placement_paper_detail.html', 'Paper Detail', 'placement_paper_detail'),
        ('interview_questions.html', 'Interview Questions', 'interview_questions'),
        ('interview_experiences.html', 'Interview Experiences', 'interview_experiences'),
        ('aptitude_categories.html', 'Aptitude Categories', 'aptitude_categories'),
        ('aptitude_practice.html', 'Aptitude Practice', 'aptitude_practice'),
        ('aptitude_result.html', 'Aptitude Result', 'aptitude_result'),
        ('coding_problems.html', 'Coding Problems', 'coding_problems'),
        ('coding_problem_detail.html', 'Problem Detail', 'coding_problem_detail'),
        ('coding_stats.html', 'Coding Statistics', 'coding_stats'),
        ('resume_list.html', 'My Resumes', 'resume_list'),
        ('create_resume.html', 'Create Resume', 'create_resume'),
        ('resume_detail.html', 'Resume Detail', 'resume_detail'),
        ('edit_resume.html', 'Edit Resume', 'edit_resume'),
        ('resume_templates.html', 'Resume Templates', 'resume_templates'),
        ('mock_interviews.html', 'Mock Interviews', 'mock_interviews'),
        ('start_mock_interview.html', 'Start Mock Interview', 'start_mock_interview'),
        ('mock_interview_detail.html', 'Interview Detail', 'mock_interview_detail'),
        ('mock_interview_result.html', 'Interview Result', 'mock_interview_result'),
        ('companies_list.html', 'Companies', 'companies_list'),
        ('company_detail.html', 'Company Detail', 'company_detail'),
        ('company_questions.html', 'Company Questions', 'company_questions'),
        ('company_experiences.html', 'Company Experiences', 'company_experiences'),
    ],
}

def create_stubs():
    """Create all stub templates"""
    template_dir = Path(__file__).parent / 'templates'
    
    for module, templates in TEMPLATES.items():
        module_dir = template_dir / module
        module_dir.mkdir(parents=True, exist_ok=True)
        
        for filename, title, view in templates:
            filepath = module_dir / filename
            if not filepath.exists():
                content = STUB_TEMPLATE.replace('{title}', title).replace('{view_name}', view)
                filepath.write_text(content)
                print(f'Created: {filepath}')
            else:
                print(f'Skipped: {filepath} (already exists)')

if __name__ == '__main__':
    create_stubs()
    print('All stub templates created successfully!')

