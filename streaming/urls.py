from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("movie/<slug:slug>/", views.movie_detail, name="movie_detail"),
    path("watch/<slug:slug>/", views.watch_movie, name="watch_movie"),
    path("movie/<slug:slug>/watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
    path("movie/<slug:slug>/rate/", views.rate_movie, name="rate_movie"),
    path("search/", views.search, name="search"),
]
