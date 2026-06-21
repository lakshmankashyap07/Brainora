# Brainora - Modern Campus Learning Platform

Brainora is a state-of-the-art college learning registry where students can view, bookmark, and share academic notes, assignments, exam papers, syllabus courses, campus announcements, and WhatsApp/Telegram study channels.

Designed with a sleek, responsive Glassmorphic user interface, Brainora incorporates dark theme modes, secure OTP verification, and JWT REST APIs.

---

## Technical Stack

### Frontend UI
- **HTML5 & CSS3**: Core layouts utilizing CSS Variables for real-time theme toggles.
- **Glassmorphism Design**: Frosted glass blur overlays, modern typography, and accent gradients.
- **Bootstrap 5**: Mobile-responsive responsive flexbox grids.
- **Font Awesome**: Styled dashboard iconography.
- **Chart.js**: Dynamic dashboards detailing user contribution statistics.
- **AOS (Animate on Scroll)**: Smooth fade and slider card animations.

### Backend Engine
- **Python 3.12+** & **Django 4.2+**: Model-View-Controller framework.
- **Django REST Framework & Simple JWT**: Token-based REST API access.
- **Django Crispy Forms**: Bootstrap 5 form renderer helper.
- **Python Decouple**: Environment separation via `.env`.
- **Whitenoise & Gunicorn**: Static file serving compressions and WSGI production gateways.

### Database & Storage
- **Relational Backend**: SQLite (Local development) / PostgreSQL.
- **MongoDB Atlas Integration**: PyMongo connection configurations.
- **Cloudinary / Local Media**: Cloud storage storage for uploaded PDF notes, worksheets, and profile avatars.

---

## Features

- **Email-or-Username Authentication**: Login using either username or email address.
- **OTP Account Verification**: Validates new signups and password recovery codes via email.
- **Account Protection & Lockout**: Restricts logins for 15 minutes after 5 consecutive failed password attempts.
- **Two-Factor Authentication (2FA)**: Adds a layer of security, requesting email-sent OTPs on login.
- **Global Search**: Instantly filters courses, notes, past papers, and notices from a single search box.
- **Statistics Dashboard**: Renders count modules and category graphs via Chart.js.
- **API Registry**: Emits JSON responses for resources, syllabus, and events under `/api/` with JWT authenticators.

---

## Project Structure

```text
brainora_project/           # Main settings, routing, and WSGI entry point
authentication/              # CustomUser models, forms, and custom auth backend
courses/                     # Course models, syllabus views, and semester listings
resources/                   # Notes, assignments, lab files, links, and bookmark toggles
activities/                  # College notices, calendar events, and holiday deadlines
papers/                      # Exam past papers grouped by course and year
dashboard/                   # Home views, statistics, Chart.js inputs, and seed commands
api/                         # Model serializers and JWT viewsets
templates/                   # Global HTML template folders (base layout, error screens)
static/                      # Custom CSS style sheets and theme scripts
media/                       # Uploaded files and user avatars
manage.py                    # Django management script
requirements.txt             # Python packages manifest
```

---

## Running Locally

To run the project, please consult the complete walkthrough in [GETTING_STARTED.md](file:///c:/Users/laksh/Downloads/Brainora2.0/GETTING_STARTED.md).

Quick launch:
1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py seed_data`
4. `python manage.py runserver`

---

## Deployment Guidelines (Render or Railway)

### 1. static & Media Collection
Collect static folders into a production directory before build:
```bash
python manage.py collectstatic --no-input
```
Whitenoise will serve compiled CSS/JS from `staticfiles/` automatically in production environments.

### 2. Procfile Setup
Create a file named `Procfile` in the root folder with:
```text
web: gunicorn brainora_project.wsgi --log-file -
```

### 3. Production Environment Variables
Set variables inside Render/Railway dashboard:
- `DEBUG=False`
- `SECRET_KEY=your-production-secret`
- `ALLOWED_HOSTS=your-app-domain.com`
- Set `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET` to enable Cloudinary image/PDF hosting.
