# News Agency

---

**Table of Contents**
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Database Description](#database-description)
4. [Application Description](#application-description)
5. [How to Run the Project](#how-to-run-the-project)
   - [Prerequisites](#1-prerequisites)
   - [Installation](#2-installation)
   - [Running the Application](#3-running-the-application)
6. [Technologies](#technologies)

---

## Project Overview

This project is a Django web application for managing a newsroom workspace. It allows users to browse newspapers, topics, and redactors, while authenticated users with the required permissions can manage editorial content through the admin-style CRUD interface built into the site.

The workflow includes:
1. Authentication and registration for redactors
2. Topic management for editorial categorization
3. Newspaper management with topic and publisher assignment
4. Redactor profile management and publication browsing

---

## Project Structure

```text
news-agency/
|-- app/                              # Main Django application
|   |-- migrations/                   # Database migrations
|   |-- admin.py                      # Admin site configuration
|   |-- forms.py                      # Django forms for auth and CRUD
|   |-- models.py                     # Topic, Redactor, and Newspaper models
|   |-- tests.py                      # Test suite
|   |-- urls.py                       # Application URL routes
|   |-- views.py                      # Function-based and class-based views
|   `-- __init__.py
|-- config/                           # Django project configuration
|   |-- settings.py                   # Project settings
|   |-- urls.py                       # Root URL configuration
|   |-- asgi.py                       # ASGI entrypoint
|   |-- wsgi.py                       # WSGI entrypoint
|   `-- __init__.py
|-- static/
|   `-- css/
|       `-- styles.css                # Global application styles
|-- templates/
|   |-- app/                          # App templates
|   |-- includes/                     # Shared partial templates
|   `-- registration/                 # Login and registration templates
|-- db.sqlite3                        # SQLite database
|-- manage.py                         # Django management entrypoint
|-- README.md
|-- README_example.md
`-- requirements.txt                  # Project dependencies
```

---

## Database Description

The project uses SQLite as the default database and includes three main models:

- **Topic**
  - Stores editorial categories
  - Contains a unique `name` field

- **Redactor**
  - Custom user model based on Django `AbstractUser`
  - Stores authentication data and `years_of_experience`

- **Newspaper**
  - Stores article data
  - Includes `title`, `content`, and `published_date`
  - Belongs to one `Topic`
  - Can have multiple `publishers` from `Redactor`

Relationships:
- One `Topic` -> many `Newspaper`
- Many `Redactor` -> many `Newspaper`

---

## Application Description

The application is built with Django generic views and Bootstrap-based templates.

- Public features
  - Browse dashboard statistics
  - View topic list
  - View newspaper list and details
  - View redactor list and details

- Auth features
  - Login and logout
  - Register a new redactor account

- Management features
  - Topic CRUD for users with topic permissions
  - Newspaper CRUD for users with newspaper permissions
  - Redactor self update/delete for users with redactor permissions

The project also includes Django admin configuration for managing all core entities through `/admin/`.

---

## How to Run the Project

Follow these steps to set up the project on your local machine.

### 1. Prerequisites

- Python 3.12+
- Git
- Virtual environment tool (`venv`)

### 2. Installation

2.1. Clone the repository:

```commandline
git clone https://github.com/mishagitcode/news-agency
```

```commandline
cd news-agency
```

2.2. Create a virtual environment:

```commandline
python -m venv venv
```

2.3. Activate the virtual environment

2.3.1. Windows:

```commandline
venv\Scripts\activate
```

2.3.2. macOS/Linux:

```commandline
source venv/bin/activate
```

2.4. Install dependencies:

```commandline
pip install -r requirements.txt
```

2.5. Create `config/.config_env` and add your Django secret key:

```env
DJANGO_SECRET_KEY=your_secret_key
```

2.6. Apply migrations:

```commandline
python manage.py migrate
```

2.7. Optionally create a superuser:

```commandline
python manage.py createsuperuser
```

---

### 3. Running the Application

Start the Django development server:

```bash
python manage.py runserver
```

Open in browser:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

---

## Technologies

- **Python**: Core programming language
- **Django**: Main web framework
- **SQLite**: Default database
- **Bootstrap 5**: UI styling and responsive layout
- **HTML/CSS**: Template markup and custom styling
- **python-dotenv**: Environment variable loading

---

Developed by [mishagitcode](https://github.com/mishagitcode)
