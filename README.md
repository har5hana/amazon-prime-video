# Prime Video Clone — Django

A Prime Video-inspired streaming web application built with Django.

## Features

- Django ORM and admin
- User registration/login/logout
- Superuser/admin management
- Movies and series
- Genres
- Featured content
- Search
- Watchlist
- Watch history
- Ratings
- Poster/backdrop/video uploads
- Responsive UI
- Static files with WhiteNoise
- Automated tests

## Local setup

### 1. Create virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment

Copy `.env.example` to `.env` and set a strong `DJANGO_SECRET_KEY`.

### 4. Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create admin

```bash
python manage.py createsuperuser
```

### 6. Run

```bash
python manage.py runserver
```

Open:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/

## Production

Do not deploy with `DEBUG=True` or SQLite for a serious production deployment.

Set:
```env
DEBUG=False
DJANGO_SECRET_KEY=<strong-random-secret>
ALLOWED_HOSTS=<your-domain>
```

Use PostgreSQL and object storage/CDN for production media. Run:

```bash
python manage.py collectstatic --noinput
gunicorn primevideo.wsgi:application
```

## Important media note

The development server can serve uploaded media locally. Production video delivery should use object storage/CDN and a proper streaming architecture rather than relying on Django to serve large MP4 files.
