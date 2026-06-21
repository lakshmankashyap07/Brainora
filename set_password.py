#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brainora_project.settings')
django.setup()

from authentication.models import CustomUser

user = CustomUser.objects.get(username='admin')
user.set_password('admin123')
user.save()
print("✓ Password updated for admin user: admin / admin123")
