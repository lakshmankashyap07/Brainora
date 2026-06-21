#!/usr/bin/env python
"""Generate stub templates for college module views"""

import os
from pathlib import Path

# Template stub
STUB_TEMPLATE = """{% extends 'base.html' %}
{% block title %}{title} - Brainora{% endblock %}
{% block content %}
<div class="container py-4">
    <div class="glass-panel p-5">
        <h1 class="text-gradient">{title}</h1>
        <p class="text-secondary mt-3">This template will be implemented soon.</p>
    </div>
</div>
{% endblock %}
"""

# List of college templates to create
TEMPLATES = [
    ('announcement_list.html', 'Announcements'),
    ('announcement_detail.html', 'Announcement Detail'),
    ('event_list.html', 'Events'),
    ('event_detail.html', 'Event Detail'),
    ('club_list.html', 'Clubs'),
    ('club_detail.html', 'Club Detail'),
    ('workshop_list.html', 'Workshops'),
    ('workshop_detail.html', 'Workshop Detail'),
    ('workshop_feedback.html', 'Workshop Feedback'),
    ('lost_found_list.html', 'Lost & Found'),
    ('lost_found_form.html', 'Report Lost/Found Item'),
    ('lost_found_detail.html', 'Lost/Found Detail'),
    ('complaint_list.html', 'Complaints & Suggestions'),
    ('complaint_form.html', 'Submit Complaint'),
    ('complaint_detail.html', 'Complaint Detail'),
    ('faculty_list.html', 'Faculty Directory'),
    ('faculty_detail.html', 'Faculty Profile'),
    ('campus_map.html', 'Campus Map'),
    ('campus_location_detail.html', 'Campus Location'),
]

def create_stubs():
    """Create all stub templates"""
    template_dir = Path(__file__).parent / 'templates' / 'college'
    template_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, title in TEMPLATES:
        filepath = template_dir / filename
        if not filepath.exists():
            content = STUB_TEMPLATE.replace('{title}', title)
            filepath.write_text(content)
            print(f'Created: {filepath}')
        else:
            print(f'Skipped: {filepath} (already exists)')

if __name__ == '__main__':
    create_stubs()
    print('All stub templates created successfully!')
