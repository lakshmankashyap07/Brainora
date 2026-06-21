# Getting Started with Brainora

Brainora is a modern campus learning platform built with Django 4.2+ and Bootstrap 5. This guide will walk you through setting up the project locally for development.

## System Prerequisites
- **Python**: Python 3.12 or newer
- **Virtual Environment Tool**: `venv` (pre-bundled with Python)

---

## Installation & Environment Setup

### 1. Clone the Repository & Open Project Directory
```bash
git clone <repository-url>
cd Brainora
```

### 2. Initialize Virtual Environment
On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## Configuration (`.env`)

Create a `.env` file in the root directory (based on `.env.example` template):

```ini
# Django Configuration
SECRET_KEY=your-secure-secret-key-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
# Set USE_MONGODB=True to use MongoDB Atlas (Djongo/PyMongo settings).
# By default, SQLite is used out-of-the-box for seamless local setup.
USE_MONGODB=False
MONGODB_NAME=brainora_db
MONGODB_HOST=your-mongodb-atlas-connection-string

# Email SMTP Settings (For Password Resets & OTP)
# In DEBUG mode, Django outputs emails directly to the terminal console.
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_app_password

# Cloudinary Credentials (Optional - uploads save locally if empty)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

---

## MongoDB Atlas Integration

Brainora supports MongoDB Atlas natively for direct database queries, document logs, and JSON APIs via PyMongo.

1. Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Set up a database user and whitelist your network IP address.
3. Retrieve your application connection string.
4. Open `.env` and set `MONGODB_HOST=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority`.
5. Set `USE_MONGODB=True`.

---

## Database Migrations & Seeding

### 1. Generate & Run Database Tables
```bash
python manage.py makemigrations authentication courses resources activities papers api
python manage.py migrate
```

### 2. Populate Sample Data (Instructors, Courses, Notes, Announcements)
Run the custom seed command to populate a rich set of study materials:
```bash
python manage.py seed_data
```
*Note: This command will automatically define a superuser for you: `admin` with password `adminpassword123`.*

### 3. Creating a Custom Superuser
To create your own custom administrative credentials, run:
```bash
python manage.py createsuperuser
```

---

## Starting the Server

Launch the development web server:
```bash
python manage.py runserver
```

Once running, navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

- **Admin Dashboard**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Default Seeding Admin**: `admin` / `adminpassword123`
- **Default Seeding Student**: `john_doe` / `studentpassword123`

---

## Automated Verification

Verify setup and run test cases using Django's test runner:
```bash
python manage.py test
```
