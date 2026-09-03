from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Genre, Movie, Watchlist

class StreamingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="StrongPass123!")
        self.genre = Genre.objects.create(name="Action", slug="action")
        self.movie = Movie.objects.create(
            title="Test Movie",
            slug="test-movie",
            description="A test movie.",
            content_type="MOVIE",
            release_year=2026,
            rating=4.0,
            age_rating="13+",
        )
        self.movie.genres.add(self.genre)

    def test_home_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_movie_detail_loads(self):
        response = self.client.get(self.movie.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_watch_requires_login(self):
        response = self.client.get(reverse("watch_movie", kwargs={"slug": self.movie.slug}))
        self.assertRedirects(response, f"{reverse('login')}?next=/watch/{self.movie.slug}/")

    def test_watchlist_requires_post(self):
        self.client.login(username="tester", password="StrongPass123!")
        response = self.client.post(
            reverse("toggle_watchlist", kwargs={"slug": self.movie.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Watchlist.objects.filter(user=self.user, movie=self.movie).exists())
