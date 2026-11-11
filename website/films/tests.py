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


class FilmBehaviourTests(SmokeTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nineties = Decade.objects.create(title="The Nineties", description="<p>d</p>", year=1990)
        cls.early = Decade.objects.create(title="The Early Years", description="<p>d</p>", year=1900)
        cls.heat = Movie.objects.create(title="Heat", synopsis="<p>s</p>", review="<p>r</p>", genre="thriller",
                                        release_year=1995, decade=cls.nineties, image=tiny_image())
        cls.hidden = Movie.objects.create(title="Hidden Draft", synopsis="<p>s</p>", review="<p>r</p>", genre="drama",
                                          release_year=1996, decade=cls.nineties, image=tiny_image(), is_published=False)
        cls.birth = Movie.objects.create(title="Birth Of A Nation", synopsis="<p>s</p>", review="<p>r</p>", genre="war",
                                         release_year=1915, decade=cls.early, image=tiny_image())

    def test_movie_requested_under_the_wrong_decade_redirects_to_the_right_one(self):
        # Regression: the redirect used reverse("movie_detail") without the "films:" namespace (a 500).
        response = self.client.get(reverse("films:movie_detail", kwargs={"year": 1980, "slug": "heat"}))
        self.assertRedirects(
            response, reverse("films:movie_detail", kwargs={"year": 1990, "slug": "heat"}), fetch_redirect_response=False)

    def test_unpublished_movies_are_hidden_everywhere(self):
        self.assertEqual(
            self.client.get(reverse("films:movie_detail", kwargs={"year": 1990, "slug": "hidden-draft"})).status_code, 404)
        page = self.client.get(reverse("films:decade_view", kwargs={"year": 1990}))
        self.assertContains(page, "Heat")
        self.assertNotContains(page, "Hidden Draft")

    def test_movie_page_works_for_a_film_outside_the_top_250(self):
        page = self.client.get(reverse("films:movie_detail", kwargs={"year": 1990, "slug": "heat"}))
        self.assertEqual(page.status_code, 200)
        self.assertIsNone(page.context["top250_rank"])

    def test_the_1900s_page_covers_1900_to_1929(self):
        page = self.client.get(reverse("films:decade_view", kwargs={"year": 1900}))
        self.assertContains(page, "Birth Of A Nation")

    def test_top250_is_ordered_by_rank(self):
        second = Movie.objects.create(title="Casino", synopsis="<p>s</p>", review="<p>r</p>", genre="drama",
                                      release_year=1995, decade=self.nineties, image=tiny_image())
        Top250Entry.objects.create(movie=self.heat, rank=2)
        Top250Entry.objects.create(movie=second, rank=1)
        page = self.client.get(reverse("films:top_250")).content.decode()
        self.assertLess(page.index("Casino"), page.index("Heat"))


class FilmModelTests(SmokeTestCase):
    def test_get_decade(self):
        def decade(year):
            return Movie(release_year=year).get_decade()

        self.assertEqual(decade(1895), 1890)
        self.assertEqual(decade(1900), 1900)
        self.assertEqual(decade(1929), 1900)  # 1900-1929 share one "decade"
        self.assertEqual(decade(1930), 1930)
        self.assertEqual(decade(1999), 1990)

    def test_slug_comes_from_the_title(self):
        movie = Movie.objects.create(title="Mr. Smith Goes to Washington", synopsis="s", review="r",
                                     genre="drama", release_year=1939, image=tiny_image())
        self.assertEqual(movie.slug, "mr-smith-goes-to-washington")

    def test_top250_rank_is_none_without_an_entry(self):
        movie = Movie.objects.create(title="Solo", synopsis="s", review="r", genre="drama",
                                     release_year=2001, image=tiny_image())
        self.assertIsNone(movie.top250_rank)
        Top250Entry.objects.create(movie=movie, rank=7)
        movie = Movie.objects.get(pk=movie.pk)
        self.assertEqual(movie.top250_rank, 7)
        self.assertEqual(str(movie.top250_entry), "#7 - Solo")

    def test_decade_helpers(self):
        decade = Decade.objects.create(title="D", description="d", year=1980)
        self.assertEqual(str(decade), "1980s")
        self.assertEqual(decade.decade_range, "1980s - 1989")
