from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe


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
