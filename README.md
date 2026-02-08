# Brainora - Learning Platform

A modern, feature-rich learning platform built with Django for college students to upload, download, and share documents, assignments, and college updates.

## Features

- **User Authentication**: Secure login and signup system with custom user model
- **Profile Management**: Extended user profiles with college ID and semester info
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Modern UI**: Beautiful gradient backgrounds and smooth animations
- **User Dashboard**: Personalized dashboard for authenticated users

## Project Structure

```
brainora_project/
├── brainora/                 # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── authentication/           # Authentication app
│   ├── templates/
│   │   ├── base.html
│   │   └── authentication/
│   │       ├── login.html
│   │       ├── signup.html
│   │       └── dashboard.html
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── static/                   # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── manage.py
└── db.sqlite3               # Database (created after migrations)
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual Environment (recommended)

## Installation & Setup

### 1. Create a Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Navigate to Project Directory

```bash
cd brainora_project
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Collect Static Files (Optional, for production)

```bash
python manage.py collectstatic
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000**

## Available URLs

- **Login Page**: http://127.0.0.1:8000/auth/login/
- **Signup Page**: http://127.0.0.1:8000/auth/signup/
- **Dashboard**: http://127.0.0.1:8000/auth/dashboard/
- **Logout**: http://127.0.0.1:8000/auth/logout/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Default Test Credentials

After creating a superuser, you can:
1. Log in with your superuser account
2. Access the admin panel to create more users
3. Sign up new users through the signup page

## Customization

### Changing the Secret Key (Important for Production)

Edit `brainora_project/brainora/settings.py`:

```python
SECRET_KEY = 'your-new-secret-key-here'
```

Generate a secure key using:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Changing Database

To use PostgreSQL instead of SQLite, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'brainora_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then install the PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

## Technology Stack

- **Backend**: Django 4.2.8
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (default), PostgreSQL (recommended for production)
- **Styling**: Custom CSS with Bootstrap components

## Future Features

- [ ] Document upload and sharing
- [ ] Assignment management
- [ ] College update notifications
- [ ] User profile customization
- [ ] File versioning
- [ ] Search functionality
- [ ] Discussion forums
- [ ] Direct messaging
- [ ] Role-based access control (Student, Teacher, Admin)

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:
```bash
python manage.py runserver 8001
```

### Static Files Not Loading

Run:
```bash
python manage.py collectstatic --noinput
```

### Database Issues

Reset the database:
```bash
python manage.py flush
python manage.py migrate
```

## Development Tips

1. **Enable Debug Toolbar** (Recommended):
   ```bash
   pip install django-debug-toolbar
   ```

2. **Create Database Backup**:
   ```bash
   python manage.py dumpdata > backup.json
   ```

3. **Load Database from Backup**:
   ```bash
   python manage.py loaddata backup.json
   ```

## Security Considerations

- **Never commit `.env` files** with sensitive data
- **Always use HTTPS** in production
- **Change the SECRET_KEY** before deploying
- **Set DEBUG = False** in production
- **Use environment variables** for sensitive settings
- **Implement CSRF protection** (already configured)
- **Use strong passwords** and two-factor authentication

## Deployment

For production deployment, refer to:
- [Django Deployment Guide](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [PythonAnywhere](https://www.pythonanywhere.com/)
- [Heroku](https://www.heroku.com/)
- [AWS](https://aws.amazon.com/)

## Contributors

- Your Name

## License

MIT License - Feel free to use this project for educational purposes.

## Support

For issues, questions, or suggestions, please create an issue in the project repository.

---

**Happy Learning with Brainora!** 🧠
