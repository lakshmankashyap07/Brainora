import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brainora.settings')
django.setup()

from authentication.models import CustomUser

username = 'testuser'
email = 'testuser@example.com'
password = 'TestPass123'

if CustomUser.objects.filter(username=username).exists():
    print('user exists')
else:
    user = CustomUser.objects.create_user(username=username, email=email, password=password)
    user.first_name = 'Test'
    user.semester = 1
    user.save()
    print('created')

print(f'username={username} password={password}')
