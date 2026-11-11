from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe
from website.testing import SmokeTestCase, tiny_image


class RecipeApiTests(TestCase):
    """The public recipes API is read-only and only shows published recipes."""

    @classmethod
    def setUpTestData(cls):
        cls.published = Recipe.objects.create(
            title="Apple Pie", ingredients="<p>apples</p>", directions="<p>bake</p>",
            category="dessert", is_published=True,
        )
        cls.draft = Recipe.objects.create(
            title="Secret Draft", ingredients="<p>x</p>", directions="<p>y</p>", is_published=False,
        )

    def test_list_returns_only_published(self):
        response = self.client.get(reverse("recipe-list"))
        self.assertEqual(response.status_code, 200)
        slugs = [r["slug"] for r in response.json()["results"]]
        self.assertEqual(slugs, ["apple-pie"])

    def test_list_has_the_fields_the_frontend_uses(self):
        item = self.client.get(reverse("recipe-list")).json()["results"][0]
        for field in ("id", "title", "slug", "description", "ingredients", "directions",
                      "category", "image_url", "total_time", "is_published"):
            self.assertIn(field, item)
        self.assertIsNone(item["image_url"])

    def test_detail_returns_published_recipe(self):
        response = self.client.get(reverse("recipe-detail", kwargs={"slug": "apple-pie"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Apple Pie")

    def test_detail_unknown_or_unpublished_is_404(self):
        for slug in ("no-such-recipe", "secret-draft"):
            response = self.client.get(reverse("recipe-detail", kwargs={"slug": slug}))
            self.assertEqual(response.status_code, 404, slug)

    def test_anonymous_cannot_write(self):
        # Refused (the default DRF permission denies anonymous writes before the view is reached,
        # 401/403) and, even if it were reached, the views have no write methods (405).
        list_url = reverse("recipe-list")
        detail_url = reverse("recipe-detail", kwargs={"slug": "apple-pie"})
        payload = {"title": "Hacked", "ingredients": "x", "directions": "y"}
        refused = (401, 403, 405)
        self.assertIn(self.client.post(list_url, payload, content_type="application/json").status_code, refused)
        for method in ("put", "patch"):
            response = getattr(self.client, method)(detail_url, payload, content_type="application/json")
            self.assertIn(response.status_code, refused, method)
        self.assertIn(self.client.delete(detail_url).status_code, refused)
        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(Recipe.objects.get(pk=self.published.pk).title, "Apple Pie")

    def test_even_a_logged_in_admin_cannot_write_through_the_api(self):
        # Recipes are edited in the Django admin; the API views have no write methods at all.
        from django.contrib.auth import get_user_model
        admin = get_user_model().objects.create_superuser("admin", "admin@example.com", "pw-for-tests")
        self.client.force_login(admin)
        payload = {"title": "Via API", "ingredients": "x", "directions": "y"}
        self.assertEqual(
            self.client.post(reverse("recipe-list"), payload, content_type="application/json").status_code, 405
        )
        self.assertEqual(
            self.client.delete(reverse("recipe-detail", kwargs={"slug": "apple-pie"})).status_code, 405
        )
        self.assertEqual(Recipe.objects.count(), 2)


class RecipeModelTests(TestCase):
    def test_slug_is_generated_from_the_title(self):
        recipe = Recipe.objects.create(title="Granny's Cinnamon Buns", ingredients="x", directions="y")
        self.assertEqual(recipe.slug, "grannys-cinnamon-buns")

    def test_an_explicit_slug_is_kept(self):
        recipe = Recipe.objects.create(title="Pie", slug="custom-slug", ingredients="x", directions="y")
        self.assertEqual(recipe.slug, "custom-slug")

    def test_total_time_needs_both_prep_and_cook(self):
        self.assertEqual(Recipe(prep_time=10, cook_time=35).get_total_time(), 45)
        self.assertIsNone(Recipe(prep_time=10).get_total_time())
        self.assertIsNone(Recipe(cook_time=35).get_total_time())
        self.assertIsNone(Recipe().get_total_time())

    def test_str_and_default_ordering_newest_first(self):
        older = Recipe.objects.create(title="Older", ingredients="x", directions="y")
        newer = Recipe.objects.create(title="Newer", ingredients="x", directions="y")
        self.assertEqual(str(older), "Older")
        self.assertEqual(list(Recipe.objects.all()), [newer, older])


class RecipeApiQueryTests(TestCase):
    """Search, filters, ordering and pagination of the public list endpoint."""

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title="Apple Pie", description="<p>Classic dessert</p>", ingredients="x",
                              directions="y", category="dessert", difficulty="easy", rating=5)
        Recipe.objects.create(title="Beef Chili", description="<p>Spicy dinner</p>", ingredients="x",
                              directions="y", category="dinner", difficulty="medium", rating=3)
        Recipe.objects.create(title="Cheesecake", description="<p>Rich dessert</p>", ingredients="x",
                              directions="y", category="dessert", difficulty="hard", rating=4)
        cls.url = reverse("recipe-list")

    def titles(self, **params):
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, 200, params)
        return [r["title"] for r in response.json()["results"]]

    def test_search_matches_title_and_description(self):
        # Regression: search_fields once named a field that does not exist, so any ?search= was a 500.
        self.assertEqual(self.titles(search="chili"), ["Beef Chili"])
        self.assertEqual(sorted(self.titles(search="dessert")), ["Apple Pie", "Cheesecake"])
        self.assertEqual(self.titles(search="no-such-thing"), [])

    def test_filters(self):
        self.assertEqual(sorted(self.titles(category="dessert")), ["Apple Pie", "Cheesecake"])
        self.assertEqual(self.titles(difficulty="medium"), ["Beef Chili"])
        self.assertEqual(self.titles(rating=4), ["Cheesecake"])
        self.assertEqual(self.titles(category="dessert", difficulty="hard"), ["Cheesecake"])

    def test_ordering(self):
        self.assertEqual(self.titles(ordering="title"), ["Apple Pie", "Beef Chili", "Cheesecake"])
        self.assertEqual(self.titles(ordering="-title"), ["Cheesecake", "Beef Chili", "Apple Pie"])
        self.assertEqual(self.titles(ordering="-rating"), ["Apple Pie", "Cheesecake", "Beef Chili"])
        self.assertEqual(self.titles(), ["Cheesecake", "Beef Chili", "Apple Pie"])  # default: newest first

    def test_response_is_paginated_with_the_expected_envelope(self):
        data = self.client.get(self.url).json()
        self.assertEqual(set(data), {"count", "next", "previous", "results"})
        self.assertEqual(data["count"], 3)
        self.assertIsNone(data["next"])

    def test_pages_hold_20_recipes_and_unknown_pages_are_404(self):
        for n in range(22):
            Recipe.objects.create(title=f"Filler {n:02d}", ingredients="x", directions="y")
        first = self.client.get(self.url).json()
        self.assertEqual(first["count"], 25)
        self.assertEqual(len(first["results"]), 20)
        self.assertIsNotNone(first["next"])
        second = self.client.get(self.url, {"page": 2}).json()
        self.assertEqual(len(second["results"]), 5)
        self.assertEqual(self.client.get(self.url, {"page": 99}).status_code, 404)


class RecipeSerializerTests(SmokeTestCase):
    def test_image_url_is_absolute_and_total_time_is_computed(self):
        recipe = Recipe.objects.create(
            title="With Picture", ingredients="x", directions="y", prep_time=15, cook_time=30, image=tiny_image())
        item = self.client.get(reverse("recipe-detail", kwargs={"slug": recipe.slug})).json()
        self.assertEqual(item["total_time"], 45)
        self.assertTrue(item["image_url"].startswith("http://testserver/media/recipe_images/"), item["image_url"])
