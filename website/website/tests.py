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

    def test_retired_blog_has_no_admin_entry(self):
        from django.urls import NoReverseMatch
        with self.assertRaises(NoReverseMatch):
            reverse("admin:blog_article_changelist")


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
        from films.models import Decade, Movie
        from portfolio.models import Project
        from recipes.models import Recipe
        from website.testing import tiny_image

        cls.admin = get_user_model().objects.create_superuser("admin", "admin@example.com", "pw-for-tests")
        cls.objects = {
            "portfolio_project": Project.objects.create(
                title="P", subtitle="s", description="<p>d</p>", image=tiny_image(), lessons_learned="<ul><li>x</li></ul>"),
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


class SharedBaseTemplateTests(SmokeTestCase):
    """Every public page uses the one base template: same nav, footer, favicon and <head> metadata."""

    @classmethod
    def setUpTestData(cls):
        from films.models import Decade, Movie, Top250Entry
        from portfolio.models import Project
        from website.testing import tiny_image

        project = Project.objects.create(
            title="Callback", subtitle="Resume tailoring", description="<p>Writes resumes.</p>", image=tiny_image())
        decade = Decade.objects.create(title="The Nineties", description="<p>Decade</p>", year=1990)
        movie = Movie.objects.create(
            title="Heat", synopsis="<p>Cops and robbers</p>", review="<p>Great</p>", genre="thriller",
            release_year=1995, decade=decade, image=tiny_image())
        Top250Entry.objects.create(movie=movie, rank=1)
        cls.urls = [
            reverse("portfolio"),
            project.get_absolute_url(),
            reverse("films:top_250"),
            reverse("films:decade_view", kwargs={"year": 1990}),
            reverse("films:movie_detail", kwargs={"year": 1990, "slug": movie.slug}),
            reverse("projects"),
        ]

    def test_every_public_page_has_the_shared_nav_footer_and_metadata(self):
        for url in self.urls:
            with self.subTest(url=url):
                page = self.client.get(url).content.decode()
                self.assertEqual(page.count('class="site-nav"'), 1)
                self.assertEqual(page.count('class="site-footer"'), 1)
                self.assertIn('<meta charset="UTF-8">', page)
                self.assertRegex(page, r'<meta name="description" content="[^"]{5,}">')
                self.assertRegex(page, r'<meta property="og:title" content="[^"]+">')
                self.assertIn('property="og:image" content="https://christiandonovan.ca/static/images/og-default.png"', page)
                self.assertIn(f'<link rel="canonical" href="https://christiandonovan.ca{url}">', page)
                self.assertIn('rel="icon" type="image/svg+xml" href="/static/favicon/favicon.svg"', page)
                self.assertIn('rel="apple-touch-icon" href="/static/favicon/apple-touch-icon.png"', page)
                self.assertNotIn("portfolio/favicon", page)
                self.assertIn('css/site.css', page)

    def test_pages_are_valid_documents_with_nothing_outside_the_body(self):
        # Regression: base.html used to put <nav> between </head> and <body>.
        for url in self.urls:
            with self.subTest(url=url):
                page = self.client.get(url).content.decode()
                self.assertLess(page.index("<body>"), page.index("<nav"))
                self.assertTrue(page.rstrip().endswith("</html>"))
                self.assertEqual(page.count("<html"), 1)

    def test_pages_load_no_third_party_fonts_and_no_inline_script(self):
        for url in self.urls:
            with self.subTest(url=url):
                page = self.client.get(url).content.decode()
                self.assertNotIn("fonts.googleapis.com", page)
                self.assertNotIn("fonts.gstatic.com", page)
                # scripts are allowed only as external files (keeps a Content-Security-Policy possible)
                self.assertNotRegex(page, r"<script(?![^>]*\ssrc=)")
                self.assertNotRegex(page, r'\son[a-z]+="')

    def test_page_titles_and_descriptions_come_from_the_content(self):
        project_page = self.client.get(self.urls[1]).content.decode()
        self.assertIn("<title>Callback | Christian Arbelaez</title>", project_page)
        self.assertIn('<meta name="description" content="Resume tailoring">', project_page)
        movie_page = self.client.get(self.urls[4]).content.decode()
        self.assertIn("<title>Heat (1995) | Christian Arbelaez</title>", movie_page)
        self.assertIn("<title>Christian Arbelaez</title>", self.client.get(self.urls[0]).content.decode())

    def test_metadata_is_escaped(self):
        from portfolio.models import Project
        from website.testing import tiny_image
        project = Project.objects.create(
            title='A "quoted" <b>title</b>', subtitle='Sub "title"', description="<p>d</p>", image=tiny_image())
        page = self.client.get(project.get_absolute_url()).content.decode()
        self.assertIn("<title>A &quot;quoted&quot; &lt;b&gt;title&lt;/b&gt; | Christian Arbelaez</title>", page)
        self.assertIn('content="Sub &quot;title&quot;"', page)

    def test_films_pages_link_to_every_decade(self):
        page = self.client.get(reverse("films:top_250")).content.decode()
        self.assertIn('class="subnav"', page)
        self.assertIn(reverse("films:decade_view", kwargs={"year": 1990}), page)
        self.assertNotIn('class="subnav"', self.client.get(reverse("portfolio")).content.decode())

    def test_fonts_stylesheet_and_preview_image_are_static_files(self):
        from django.contrib.staticfiles import finders
        for path in [
            "css/site.css",
            "fonts/archivo-latin-wght.woff2",
            "fonts/jetbrains-mono-latin-wght.woff2",
            "fonts/OFL-Archivo.txt",
            "fonts/OFL-JetBrainsMono.txt",
            "images/og-default.png",
            "favicon/favicon.svg",
            "favicon/favicon.ico",
            "favicon/favicon-32x32.png",
            "favicon/favicon-16x16.png",
            "favicon/apple-touch-icon.png",
        ]:
            with self.subTest(path=path):
                self.assertIsNotNone(finders.find(path))

    def test_removed_templates_and_stylesheets_are_not_referenced(self):
        for url in self.urls:
            with self.subTest(url=url):
                page = self.client.get(url).content.decode()
                for gone in ["navbar.css", "footer.css", "css/base.css", "github.png", "facebook.png"]:
                    self.assertNotIn(gone, page)


class SitemapAndRobotsTests(SmokeTestCase):
    @classmethod
    def setUpTestData(cls):
        from films.models import Decade, Movie
        from portfolio.models import Project
        from website.testing import tiny_image

        Project.objects.create(title="Shown Project")
        Project.objects.create(title="Hidden Project", is_published=False)
        decade = Decade.objects.create(title="The Nineties", description="<p>d</p>", year=1990)
        Movie.objects.create(title="Heat", synopsis="<p>s</p>", review="<p>r</p>", genre="thriller",
                             release_year=1995, decade=decade, image=tiny_image())
        Movie.objects.create(title="Draft Film", synopsis="<p>s</p>", review="<p>r</p>", genre="drama",
                             release_year=1996, decade=decade, image=tiny_image(), is_published=False)

    def test_sitemap_lists_public_pages_only(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("xml", response["Content-Type"])
        body = response.content.decode()
        for path in ["/", "/projects/", "/personal/", "/films/", "/project/shown-project/", "/films/1990s/", "/films/1990s/heat/"]:
            self.assertIn(f"<loc>https://testserver{path}</loc>", body)
        for hidden in ["hidden-project", "draft-film", "/admin/", "/resume/", "/api/"]:
            self.assertNotIn(hidden, body)

    def test_every_sitemap_url_answers_200(self):
        import re
        body = self.client.get("/sitemap.xml").content.decode()
        urls = re.findall(r"<loc>https://testserver([^<]+)</loc>", body)
        self.assertGreaterEqual(len(urls), 7)
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("text/plain"))
        body = response.content.decode()
        self.assertIn("User-agent: *", body)
        self.assertIn("Disallow: /admin/", body)
        self.assertIn("Disallow: /resume/", body)
        self.assertIn("Sitemap: https://christiandonovan.ca/sitemap.xml", body)


class ContentSecurityPolicyTests(SmokeTestCase):
    REPORT, ENFORCE = "Content-Security-Policy-Report-Only", "Content-Security-Policy"

    def test_public_pages_send_the_policy_in_report_only_mode_by_default(self):
        for url in ["/", "/projects/", "/personal/", "/films/", "/robots.txt"]:
            with self.subTest(url=url):
                response = self.client.get(url)
                policy = response[self.REPORT]
                self.assertNotIn(self.ENFORCE, response)
                self.assertIn("default-src 'self'", policy)
                self.assertIn("script-src 'self'", policy)
                self.assertIn("frame-ancestors 'none'", policy)
                self.assertNotIn("unsafe-eval", policy)
                self.assertNotIn("script-src 'self' 'unsafe-inline'", policy)

    def test_admin_editor_and_api_are_exempt(self):
        for url in ["/admin/login/", "/api/v1/recipes/"]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotIn(self.REPORT, response)
                self.assertNotIn(self.ENFORCE, response)

    def test_enforce_and_off_modes(self):
        from django.test import override_settings
        with override_settings(CSP_MODE="enforce"):
            response = self.client.get("/")
            self.assertIn(self.ENFORCE, response)
            self.assertNotIn(self.REPORT, response)
        with override_settings(CSP_MODE="off"):
            response = self.client.get("/")
            self.assertNotIn(self.ENFORCE, response)
            self.assertNotIn(self.REPORT, response)

    def test_templates_have_nothing_the_policy_would_block(self):
        # No inline <style>, no inline script, no event handlers, no third-party hosts for scripts or styles.
        import re
        for url in ["/", "/projects/", "/personal/", "/films/"]:
            with self.subTest(url=url):
                page = self.client.get(url).content.decode()
                self.assertNotIn("<style", page)
                self.assertNotRegex(page, r"<script(?![^>]*\ssrc=)")
                self.assertNotRegex(page, r'\son[a-z]+="')
                for source in re.findall(r'<(?:script|link)[^>]+(?:src|href)="([^"]+)"', page):
                    self.assertTrue(source.startswith("/") or source.startswith("https://christiandonovan.ca"), source)


def picture_upload(name, size, mode="RGB", fmt="PNG", color=(200, 30, 30), frames=1):
    from io import BytesIO
    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image
    image = Image.new(mode, size, color if mode != "RGBA" else (*color, 0))
    out = BytesIO()
    if frames > 1:
        image.save(out, "GIF", save_all=True, append_images=[Image.new("RGB", size, (0, 0, 255))] * (frames - 1), duration=100)
    else:
        image.save(out, fmt)
    return SimpleUploadedFile(name, out.getvalue())


class ResizedImagesTests(SmokeTestCase):
    def movie(self, upload, title="Heat"):
        from films.models import Decade, Movie
        decade, _ = Decade.objects.get_or_create(year=1990, defaults={"title": "The Nineties", "description": "<p>d</p>"})
        return Movie.objects.create(title=title, synopsis="<p>s</p>", review="<p>r</p>", genre="thriller",
                                    release_year=1995, decade=decade, image=upload)

    def open_copy(self, image, width):
        from django.core.files.storage import default_storage
        from PIL import Image
        from website.images import resized_name
        with default_storage.open(resized_name(image.name, width), "rb") as handle:
            picture = Image.open(handle)
            picture.load()
            return picture

    def test_saving_a_movie_writes_webp_copies_at_each_width_and_keeps_the_upload(self):
        from django.core.files.storage import default_storage
        movie = self.movie(picture_upload("poster.png", (1200, 1800)))
        original = default_storage.size(movie.image.name)
        for width in [200, 500, 600]:
            copy = self.open_copy(movie.image, width)
            self.assertEqual((copy.format, copy.size), ("WEBP", (width, width * 3 // 2)))
        self.assertEqual(default_storage.size(movie.image.name), original)
        self.assertTrue(movie.image.name.endswith(".png"))

    def test_small_images_are_never_enlarged(self):
        movie = self.movie(picture_upload("small.png", (300, 450)))
        self.assertEqual(self.open_copy(movie.image, 600).size, (300, 450))
        self.assertEqual(self.open_copy(movie.image, 200).size, (200, 300))

    def test_transparency_is_kept(self):
        from portfolio.models import Project
        project = Project.objects.create(title="Logo", image=picture_upload("logo.png", (2000, 1000), mode="RGBA"))
        copy = self.open_copy(project.image, 1600)
        self.assertEqual(copy.size, (1600, 800))
        self.assertEqual(copy.convert("RGBA").getpixel((5, 5))[3], 0)

    def test_pages_use_the_copies(self):
        from films.models import Top250Entry
        from portfolio.models import Project
        movie = self.movie(picture_upload("poster.png", (1200, 1800)))
        Top250Entry.objects.create(movie=movie, rank=1)
        project = Project.objects.create(title="Shot", image=picture_upload("shot.png", (2400, 1500)))
        stem = movie.image.name.rsplit(".", 1)[0]
        self.assertContains(self.client.get("/films/"), f'src="/media/resized/200/{stem}.webp"')
        self.assertContains(self.client.get("/films/1990s/"), f'src="/media/resized/500/{stem}.webp"')
        self.assertContains(self.client.get(f"/films/1990s/{movie.slug}/"), f'src="/media/resized/600/{stem}.webp"')
        self.assertContains(self.client.get(project.get_absolute_url()),
                            f'src="/media/resized/1600/{project.image.name.rsplit(".", 1)[0]}.webp"')

    def test_page_falls_back_to_the_upload_while_there_is_no_copy(self):
        from django.core.files.storage import default_storage
        from website import images
        movie = self.movie(picture_upload("poster.png", (1200, 1800)))
        name = images.resized_name(movie.image.name, 600)
        default_storage.delete(name)
        images._known.discard(name)
        page = self.client.get(f"/films/1990s/{movie.slug}/")
        self.assertContains(page, f'src="{movie.image.url}"')
        self.assertNotContains(page, "/media/resized/600/")

    def test_animations_and_unreadable_files_are_left_alone_without_breaking_the_save(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        from website import images
        animated = self.movie(picture_upload("anim.gif", (400, 600), frames=3), title="Animated")
        broken = self.movie(SimpleUploadedFile("broken.jpg", b"this is not an image"), title="Broken")
        for movie in [animated, broken]:
            with self.subTest(movie=movie.title):
                self.assertEqual(images.resize_for(movie), [])
                page = self.client.get(f"/films/1990s/{movie.slug}/")
                self.assertContains(page, f'src="{movie.image.url}"')

    def test_no_image_renders_nothing_and_the_filter_returns_an_empty_string(self):
        from portfolio.models import Project
        from website.images import resized_url
        project = Project.objects.create(title="No Picture")
        self.assertEqual(resized_url(project.image, 1600), "")
        self.assertNotContains(self.client.get(project.get_absolute_url()), "<img")

    def test_backfill_command_dry_run_then_write_then_nothing_left(self):
        from io import StringIO
        from django.core.files.storage import default_storage
        from django.core.management import call_command
        from website import images
        movie = self.movie(picture_upload("poster.png", (1200, 1800)))
        for width in [200, 500, 600]:  # as if uploaded before this release
            default_storage.delete(images.resized_name(movie.image.name, width))
        images._known.clear()

        def run(*args):
            out = StringIO()
            call_command("resize_images", *args, stdout=out)
            return out.getvalue()

        self.assertIn("would write 3 files", run("--dry-run"))
        self.assertFalse(default_storage.exists(images.resized_name(movie.image.name, 200)))
        self.assertIn("wrote 3 files", run())
        self.assertTrue(default_storage.exists(images.resized_name(movie.image.name, 200)))
        self.assertIn("wrote 0 files", run())
        self.assertIn("wrote 3 files", run("--force"))
        # --force replaces in place: no "_abc123" duplicates
        folder = images.resized_name(movie.image.name, 200).rsplit("/", 1)[0]
        self.assertEqual(len(default_storage.listdir(folder)[1]), 1)
