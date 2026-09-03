from django.conf import settings
from django.db import models
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Movie(models.Model):
    CONTENT_TYPES = [("MOVIE", "Movie"), ("SERIES", "Series")]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    description = models.TextField()
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default="MOVIE")
    release_year = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    age_rating = models.CharField(max_length=20, default="13+")
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    poster = models.ImageField(upload_to="posters/")
    backdrop = models.ImageField(upload_to="backdrops/", blank=True, null=True)
    trailer_url = models.URLField(blank=True)
    video = models.FileField(upload_to="videos/", blank=True, null=True)
    featured = models.BooleanField(default=False)
    is_prime = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["content_type"]),
            models.Index(fields=["release_year"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.slug})

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="unique_user_movie_watchlist")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class WatchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watch_history")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watch_history")
    progress_seconds = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    last_watched = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="unique_user_movie_history")
        ]
        ordering = ["-last_watched"]

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    value = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="unique_user_movie_rating")
        ]

    def __str__(self):
        return f"{self.movie.title}: {self.value}"
