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
        list_url = reverse("recipe-list")
        detail_url = reverse("recipe-detail", kwargs={"slug": "apple-pie"})
        payload = {"title": "Hacked", "ingredients": "x", "directions": "y"}
        self.assertEqual(self.client.post(list_url, payload, content_type="application/json").status_code, 405)
        for method in ("put", "patch"):
            response = getattr(self.client, method)(detail_url, payload, content_type="application/json")
            self.assertEqual(response.status_code, 405, method)
        self.assertEqual(self.client.delete(detail_url).status_code, 405)
        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(Recipe.objects.get(pk=self.published.pk).title, "Apple Pie")
