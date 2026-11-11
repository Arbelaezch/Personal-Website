from django.urls import reverse

from films.models import Decade, Movie, Top250Entry
from website.testing import SmokeTestCase, tiny_image


class FilmPagesTests(SmokeTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.decade = Decade.objects.create(title="The Nineties", description="<p>Decade</p>", year=1990)
        cls.movie = Movie.objects.create(
            title="Heat", synopsis="<p>Cops and robbers</p>", review="<p>Great</p>", genre="thriller",
            release_year=1995, decade=cls.decade, image=tiny_image(), rating=9,
        )
        cls.decade.favorite_movies.add(cls.movie)
        Top250Entry.objects.create(movie=cls.movie, rank=1)

    def test_top250(self):
        response = self.client.get(reverse("films:top_250"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Heat")

    def test_decade_page(self):
        response = self.client.get(reverse("films:decade_view", kwargs={"year": 1990}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Heat")

    def test_movie_detail(self):
        response = self.client.get(
            reverse("films:movie_detail", kwargs={"year": 1990, "slug": self.movie.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Heat")

    def test_unknown_decade_and_movie_are_404(self):
        self.assertEqual(self.client.get(reverse("films:decade_view", kwargs={"year": 1700})).status_code, 404)
        self.assertEqual(self.client.get(reverse("films:decade_view", kwargs={"year": 2010})).status_code, 404)
        self.assertEqual(
            self.client.get(reverse("films:movie_detail", kwargs={"year": 1990, "slug": "nope"})).status_code, 404
        )
