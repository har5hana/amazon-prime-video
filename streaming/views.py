from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm
from .models import Movie, Rating, WatchHistory, Watchlist

def home(request):
    featured = Movie.objects.filter(is_active=True, featured=True).prefetch_related("genres").first()
    movies = Movie.objects.filter(is_active=True, content_type="MOVIE").prefetch_related("genres")
    series = Movie.objects.filter(is_active=True, content_type="SERIES").prefetch_related("genres")

    context = {"featured": featured, "movies": movies[:12], "series": series[:12]}

    if request.user.is_authenticated:
        context["watchlist"] = Movie.objects.filter(
            watchlisted_by__user=request.user, is_active=True
        ).prefetch_related("genres")[:12]
        context["continue_watching"] = Movie.objects.filter(
            watch_history__user=request.user,
            watch_history__completed=False,
            is_active=True,
        ).prefetch_related("genres")[:12]

    return render(request, "home.html", context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("home")
    return render(request, "register.html", {"form": form})

def movie_detail(request, slug):
    movie = get_object_or_404(
        Movie.objects.prefetch_related("genres"),
        slug=slug,
        is_active=True,
    )
    in_watchlist = request.user.is_authenticated and Watchlist.objects.filter(
        user=request.user, movie=movie
    ).exists()
    related_movies = Movie.objects.filter(
        genres__in=movie.genres.all(), is_active=True
    ).exclude(pk=movie.pk).distinct().prefetch_related("genres")[:8]
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, movie=movie).first()
    return render(request, "movie_detail.html", {
        "movie": movie,
        "in_watchlist": in_watchlist,
        "related_movies": related_movies,
        "user_rating": user_rating,
    })

@login_required
def watch_movie(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    WatchHistory.objects.get_or_create(user=request.user, movie=movie)
    return render(request, "watch.html", {"movie": movie})

@login_required
def toggle_watchlist(request, slug):
    if request.method != "POST":
        return redirect("movie_detail", slug=slug)
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    item, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)
    if created:
        messages.success(request, f"{movie.title} added to your watchlist.")
    else:
        item.delete()
        messages.info(request, f"{movie.title} removed from your watchlist.")
    return redirect(movie.get_absolute_url())

@login_required
def rate_movie(request, slug):
    if request.method != "POST":
        return redirect("movie_detail", slug=slug)
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    try:
        value = int(request.POST.get("value", "0"))
    except ValueError:
        value = 0
    if value not in range(1, 6):
        messages.error(request, "Rating must be between 1 and 5.")
        return redirect(movie.get_absolute_url())
    Rating.objects.update_or_create(
        user=request.user, movie=movie, defaults={"value": value}
    )
    aggregate = Rating.objects.filter(movie=movie).aggregate(avg=Avg("value"))["avg"]
    movie.rating = round(aggregate or 0, 1)
    movie.save(update_fields=["rating", "updated_at"])
    messages.success(request, "Rating saved.")
    return redirect(movie.get_absolute_url())

def search(request):
    query = request.GET.get("q", "").strip()
    results = Movie.objects.filter(is_active=True).prefetch_related("genres")
    if query:
        results = results.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(genres__name__icontains=query)
        ).distinct()
    return render(request, "search.html", {"query": query, "results": results})
