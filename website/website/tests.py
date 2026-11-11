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

    def test_every_editor_field_uses_a_configured_editor(self):
        # A field asking for a config name that does not exist breaks its admin page (it did once).
        from django.apps import apps
        from django_ckeditor_5.fields import CKEditor5Field

        fields = [
            (model, f)
            for model in apps.get_models()
            for f in model._meta.get_fields()
            if isinstance(f, CKEditor5Field)
        ]
        self.assertGreaterEqual(len(fields), 9)  # portfolio 2, films 3, recipes 3, blog 1
        for model, f in fields:
            with self.subTest(field=f"{model.__name__}.{f.name}"):
                self.assertIn(f.config_name, settings.CKEDITOR_5_CONFIGS)

    def test_editor_javascript_is_available_as_a_static_file(self):
        from django.contrib.staticfiles import finders

        self.assertIsNotNone(finders.find("django_ckeditor_5/dist/bundle.js"))
        self.assertIsNotNone(finders.find("django_ckeditor_5/dist/styles.css"))


class EditorTests(SmokeTestCase):
    """The rich-text editor (CKEditor 5) on every model that uses it."""

    @classmethod
    def setUpTestData(cls):
        from blog.models import Article
        from films.models import Decade, Movie
        from portfolio.models import Project
        from recipes.models import Recipe
        from website.testing import tiny_image

        cls.admin = get_user_model().objects.create_superuser("admin", "admin@example.com", "pw-for-tests")
        cls.objects = {
            "portfolio_project": Project.objects.create(
                title="P", subtitle="s", description="<p>d</p>", image=tiny_image(), lessons_learned="<ul><li>x</li></ul>"),
            "blog_article": Article.objects.create(title="A", body="<p>b</p>", subject="META"),
            "films_decade": Decade.objects.create(title="D", description="<p>d</p>", year=1990),
            "films_movie": Movie.objects.create(
                title="M", synopsis="<p>s</p>", review="<p>r</p>", genre="drama", release_year=1995, image=tiny_image()),
            "recipes_recipe": Recipe.objects.create(title="R", ingredients="<ul><li>a</li></ul>", directions="<ol><li>b</li></ol>"),
        }

    def test_change_pages_render_the_editor_for_existing_objects(self):
        self.client.force_login(self.admin)
        for name, obj in self.objects.items():
            with self.subTest(model=name):
                response = self.client.get(reverse(f"admin:{name}_change", args=[obj.pk]))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "django_ckeditor_5")
                self.assertContains(response, "ck-editor-5-upload-url")

    def test_content_saved_through_the_admin_is_stored_unchanged(self):
        # numbered-list continuation (<ol start>, <li value>), em/u/sup, entities: all in real data
        html = ('<p>Intro&nbsp;text <em>em</em> <u>u</u> x<sup>2</sup></p>'
                '<ol start="3"><li value="3">Third</li><li>Fourth</li></ol>')
        recipe = self.objects["recipes_recipe"]
        self.client.force_login(self.admin)
        url = reverse("admin:recipes_recipe_change", args=[recipe.pk])
        response = self.client.post(url, {
            "title": recipe.title, "slug": recipe.slug, "rating": "3", "description": "",
            "ingredients": "<ul><li>a</li></ul>", "directions": html, "difficulty": "medium",
            "category": "", "is_published": "on",
        })
        self.assertEqual(response.status_code, 302, getattr(response, "context", None) and response.context["adminform"].form.errors)
        recipe.refresh_from_db()
        self.assertEqual(recipe.directions, html)

    def test_image_upload_is_staff_only(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from website.testing import TINY_GIF

        url = reverse("ck_editor_5_upload_file")
        upload = lambda: {"upload": SimpleUploadedFile("t.gif", TINY_GIF, content_type="image/gif")}
        self.assertEqual(self.client.post(url, upload()).status_code, 403)  # anonymous
        regular = get_user_model().objects.create_user("regular", "r@example.com", "pw-for-tests")
        self.client.force_login(regular)
        self.assertEqual(self.client.post(url, upload()).status_code, 403)  # logged in, not staff
        self.client.force_login(self.admin)
        response = self.client.post(url, upload())
        self.assertEqual(response.status_code, 200)
        self.assertIn("url", response.json())

    def test_html_from_the_editor_is_stored_tidy(self):
        # What CKEditor 5 sends: random list-item ids and <i> for italics.
        sent = ('<p>Hello <i>there</i> <u>u</u></p>'
                '<ul><li data-list-item-id="e0123abc">one</li><li data-list-item-id="e9876fed">two</li></ul>')
        stored = ('<p>Hello <em>there</em> <u>u</u></p>'
                  '<ul><li>one</li><li>two</li></ul>')
        recipe = self.objects["recipes_recipe"]
        self.client.force_login(self.admin)
        response = self.client.post(reverse("admin:recipes_recipe_change", args=[recipe.pk]), {
            "title": recipe.title, "slug": recipe.slug, "rating": "3", "description": "",
            "ingredients": sent, "directions": "<ol><li>b</li></ol>", "difficulty": "medium",
            "category": "", "is_published": "on",
        })
        self.assertEqual(response.status_code, 302)
        recipe.refresh_from_db()
        self.assertEqual(recipe.ingredients, stored)


class CleanEditorHtmlTests(SmokeTestCase):
    def test_removes_list_item_ids_and_turns_i_into_em(self):
        from website.fields import clean_editor_html

        self.assertEqual(clean_editor_html('<li data-list-item-id="e1">x</li>'), "<li>x</li>")
        self.assertEqual(clean_editor_html("<i>a</i> and <i class=\"k\">b</i>"), "<em>a</em> and <em class=\"k\">b</em>")

    def test_leaves_other_tags_alone(self):
        from website.fields import clean_editor_html

        html = '<p>x</p><img src="a.png"><iframe></iframe><ol start="3"><li value="3">y</li></ol><sup>2</sup><br>'
        self.assertEqual(clean_editor_html(html), html)
