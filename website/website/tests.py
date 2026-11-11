"""Site-wide smoke tests: admin (CKEditor / sortable widgets) and CORS."""
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse

from website.testing import SmokeTestCase


class AdminSmokeTests(SmokeTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser("admin", "admin@example.com", "pw-for-tests")

    def test_login_page_renders_for_anonymous(self):
        self.assertEqual(self.client.get(reverse("admin:login")).status_code, 200)

    def test_admin_redirects_anonymous_to_login(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_admin_pages_render_for_superuser(self):
        self.client.force_login(self.admin)
        # change lists, and add forms that render the CKEditor / sortable widgets
        pages = [
            reverse("admin:index"),
            reverse("admin:portfolio_project_changelist"),
            reverse("admin:portfolio_project_add"),
            reverse("admin:blog_article_changelist"),
            reverse("admin:films_movie_changelist"),
            reverse("admin:films_movie_add"),
            reverse("admin:films_decade_add"),
            reverse("admin:films_top250entry_changelist"),
            reverse("admin:recipes_recipe_changelist"),
            reverse("admin:recipes_recipe_add"),
        ]
        for url in pages:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_blog_article_add_page_renders(self):
        # Regression: settings.py used to define CKEDITOR_CONFIGS twice and drop "portal_config",
        # which Article.body asks for, so this page returned 500.
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("admin:blog_article_add")).status_code, 200)


class CorsTests(SmokeTestCase):
    URL = "/api/v1/recipes/"

    def test_family_food_origin_is_allowed(self):
        response = self.client.get(self.URL, HTTP_ORIGIN="https://family-food.vercel.app")
        self.assertEqual(response["Access-Control-Allow-Origin"], "https://family-food.vercel.app")

    def test_other_origin_is_not_allowed(self):
        response = self.client.get(self.URL, HTTP_ORIGIN="https://evil.example")
        self.assertNotIn("Access-Control-Allow-Origin", response)

    def test_preflight_only_allows_read_methods(self):
        response = self.client.options(
            self.URL,
            HTTP_ORIGIN="https://family-food.vercel.app",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="DELETE",
        )
        allowed = response.get("Access-Control-Allow-Methods", "")
        for method in ("GET", "HEAD", "OPTIONS"):
            self.assertIn(method, allowed)
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            self.assertNotIn(method, allowed)


class SettingsTests(SmokeTestCase):
    def test_api_is_protected_by_default(self):
        # New views must not be writable by anonymous users unless they opt in.
        self.assertEqual(
            settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"],
            ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
        )

    def test_ckeditor_configs_include_every_named_config(self):
        # blog.Article uses "portal_config", films use "films"; a duplicate definition once lost one.
        for name in ("default", "films", "portal_config"):
            self.assertIn(name, settings.CKEDITOR_CONFIGS)
