# Prime Video Clone

A Prime Video-inspired streaming web application built using Django. The application provides user authentication, content management, movie and TV show browsing, search, watchlists, ratings, watch history, video playback, and an administration panel.

## Features

* User registration and authentication
* Login and logout
* Movie and TV show management
* Genre management
* Featured content
* Movie and TV show details
* Search functionality
* Watchlist
* Continue Watching
* Watch history
* User ratings
* Video playback
* Poster and backdrop uploads
* Django Admin panel
* Responsive user interface
* Django ORM
* Static file management with WhiteNoise
* Production WSGI configuration with Gunicorn
* Automated tests

## Technology Stack

* Python
* Django
* Django ORM
* SQLite for development
* PostgreSQL recommended for production
* HTML5
* CSS3
* Pillow
* WhiteNoise
* Gunicorn
* Git and GitHub

## Project Structure

```text
primevideo/
|
|-- manage.py
|
|-- primevideo/
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|
|-- streaming/
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- urls.py
|   |-- views.py
|   |-- tests.py
|   `-- migrations/
|
|-- templates/
|   |-- base.html
|   |-- home.html
|   |-- movie_detail.html
|   |-- watch.html
|   |-- login.html
|   |-- register.html
|   `-- search.html
|
|-- static/
|   `-- css/
|       `-- style.css
|
|-- media/
|   |-- posters/
|   |-- backdrops/
|   `-- videos/
|
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- Procfile
|-- runtime.txt
`-- README.md
```

## Database Models

### Genre

Stores movie and TV show genres.

Fields:

* name
* slug

### Movie

Stores movies and TV shows.

Fields:

* title
* slug
* description
* content type
* release year
* duration
* rating
* age rating
* genres
* poster
* backdrop
* trailer URL
* video
* featured
* Prime availability
* active status
* created timestamp
* updated timestamp

### Watchlist

Connects users with movies and TV shows.

Fields:

* user
* movie
* created timestamp

A unique constraint prevents duplicate watchlist entries.

### WatchHistory

Stores the user's viewing history.

Fields:

* user
* movie
* playback progress
* completed status
* last watched timestamp

### Rating

Stores user ratings.

Fields:

* user
* movie
* rating value
* created timestamp
* updated timestamp

A unique constraint prevents a user from creating multiple ratings for the same title.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd primevideo
```

### 2. Create a virtual environment

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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root.

Use `.env.example` as the template.

Example:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

For production:

```env
DJANGO_SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

Do not commit the `.env` file to GitHub.

## Database Setup

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

## Create Superuser

Create the Django administrator account:

```bash
python manage.py createsuperuser
```

Enter the requested username, email address, and password.

The admin panel is available at:

```text
/admin/
```

When running locally:

```text
http://127.0.0.1:8000/admin/
```

## Run the Application

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Application Routes

| Route                      | Description                  |
| -------------------------- | ---------------------------- |
| `/`                        | Homepage                     |
| `/register/`               | User registration            |
| `/login/`                  | User login                   |
| `/logout/`                 | User logout                  |
| `/search/`                 | Search content               |
| `/movie/<slug>/`           | Movie or TV show details     |
| `/watch/<slug>/`           | Video player                 |
| `/movie/<slug>/watchlist/` | Add or remove from watchlist |
| `/movie/<slug>/rate/`      | Submit a rating              |
| `/admin/`                  | Django administration        |

## Adding Content

Log in to:

```text
http://127.0.0.1:8000/admin/
```

Create genres first.

Example genres:

```text
Action
Comedy
Drama
Thriller
Sci-Fi
Romance
Documentary
Animation
```

Then create movies or TV shows from the Movie section.

For each title, provide:

* Title
* Description
* Content type
* Release year
* Duration
* Age rating
* Poster
* Backdrop
* Video
* Genres

To display a title as the homepage featured content, enable:

```text
Featured = True
```

## Media Files

Uploaded files are stored in:

```text
media/
|-- posters/
|-- backdrops/
`-- videos/
```

Posters are used for content cards.

Backdrops are used for hero sections.

Videos are used by the video player.

## Testing

Run the Django test suite:

```bash
python manage.py test
```

The test suite includes tests for:

* Homepage loading
* Movie detail pages
* Authentication-protected pages
* Watchlist functionality

## Static Files

Before production deployment, collect static files:

```bash
python manage.py collectstatic --noinput
```

WhiteNoise is configured to serve collected static files.

## Production Deployment

Before deploying, run:

```bash
python manage.py check --deploy
```

Set:

```env
DEBUG=False
DJANGO_SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com
```

Collect static files:

```bash
python manage.py collectstatic --noinput
```

Start the application with Gunicorn:

```bash
gunicorn primevideo.wsgi:application
```

## Production Database

SQLite is intended for development and testing.

For production, PostgreSQL should be used.

The recommended production architecture is:

```text
Client
   |
   v
Reverse Proxy / CDN
   |
   v
Django + Gunicorn
   |
   +---------> PostgreSQL
   |
   +---------> Object Storage
```

## Production Media Storage

Large video files should not be served directly from Django in a production environment.

Use object storage and a CDN such as:

* Amazon S3
* CloudFront
* Google Cloud Storage
* Azure Blob Storage
* Cloudinary
* Other S3-compatible storage

Django should handle application logic, authentication, authorization, and database operations while the CDN/object-storage layer handles large media delivery.

## Security Checklist

Before deploying:

* Set `DEBUG=False`
* Use a strong `DJANGO_SECRET_KEY`
* Configure `ALLOWED_HOSTS`
* Enable HTTPS
* Use PostgreSQL
* Configure production media storage
* Run `collectstatic`
* Keep database credentials in environment variables
* Do not commit `.env`
* Do not commit passwords or secret keys
* Run `python manage.py check --deploy`

## Future Improvements

* Django REST Framework API
* React or Next.js frontend
* JWT authentication
* Multiple user profiles
* Subscription management
* Payment integration
* Recommendation system
* Personalized content
* Redis caching
* Celery background jobs
* PostgreSQL
* S3 media storage
* CDN integration
* HLS adaptive video streaming
* Subtitle support
* Multiple audio tracks
* Docker
* GitHub Actions CI/CD
* Automated cloud deployment

## Disclaimer

This project is an educational Prime Video-inspired implementation. It is not affiliated with Amazon and does not include Amazon's proprietary source code, infrastructure, trademarks, or copyrighted media.

Only upload and distribute media for which you have the necessary rights or permission.
