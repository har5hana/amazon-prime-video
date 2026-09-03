from django.contrib import admin
from .models import Genre, Movie, Rating, WatchHistory, Watchlist

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "content_type", "release_year", "rating", "is_prime", "featured", "is_active")
    list_filter = ("content_type", "is_prime", "featured", "is_active", "release_year")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("genres",)
    list_editable = ("featured", "is_active", "is_prime")

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "created_at")
    search_fields = ("user__username", "movie__title")

@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "progress_seconds", "completed", "last_watched")
    list_filter = ("completed",)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "value", "created_at")
    list_filter = ("value",)
