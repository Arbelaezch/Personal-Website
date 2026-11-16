from django.contrib.auth import get_user_model
from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from django.urls import reverse

from portfolio.models import Project
from website.testing import SmokeTestCase, tiny_image


def make_project(title="Callback", **fields):
    fields.setdefault("subtitle", "Resume tailoring")
    fields.setdefault("description", "<p>Writes resumes.</p>")
    return Project.objects.create(title=title, **fields)


class PortfolioPagesTests(SmokeTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = make_project(lessons_learned="Ship small.", image=tiny_image(), order=1)

    def test_home_lists_projects(self):
        response = self.client.get(reverse("portfolio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Callback")
        self.assertContains(response, 'href="/project/callback/"')

    def test_project_detail(self):
        response = self.client.get("/project/callback/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Callback")

    def test_unknown_project_is_404(self):
        self.assertEqual(self.client.get("/project/nope/").status_code, 404)
        self.assertEqual(self.client.get(reverse("project_by_id", kwargs={"pk": 9999})).status_code, 404)

    def test_old_id_url_redirects_permanently_to_the_slug_url(self):
        response = self.client.get(f"/project/{self.project.pk}/")
        self.assertRedirects(response, "/project/callback/", status_code=301, fetch_redirect_response=False)


class ProjectOrderingTests(SmokeTestCase):
    def test_home_lists_the_highest_order_first_and_str_is_the_title(self):
        low = make_project("LowOrder", image=tiny_image(), order=1)
        high = make_project("HighOrder", image=tiny_image(), order=9)
        page = self.client.get(reverse("portfolio")).content.decode()
        self.assertLess(page.index("HighOrder"), page.index("LowOrder"))
        self.assertEqual(str(low), "LowOrder")
        self.assertEqual(str(high), "HighOrder")


class ProjectSlugTests(SmokeTestCase):
    def test_slug_is_built_from_the_title(self):
        self.assertEqual(make_project("NBA Draft Simulator").slug, "nba-draft-simulator")

    def test_duplicate_titles_get_numbered_slugs(self):
        slugs = [make_project("Apple Pie").slug for _ in range(3)]
        self.assertEqual(slugs, ["apple-pie", "apple-pie-2", "apple-pie-3"])

    def test_title_with_nothing_sluggable_falls_back(self):
        self.assertEqual(make_project("!!!").slug, "project")
        self.assertEqual(make_project("日本語").slug, "project-2")

    def test_slug_is_never_digits_only(self):
        # /project/2048/ must stay unambiguous: digits are an old id link.
        project = make_project("2048")
        self.assertEqual(project.slug, "project-2048")
        self.assertEqual(self.client.get(project.get_absolute_url()).status_code, 200)

    def test_long_titles_are_truncated_and_stay_unique(self):
        first = make_project("word " * 60)
        second = make_project("word " * 60)
        self.assertLessEqual(len(first.slug), 80)
        self.assertLessEqual(len(second.slug), 80)
        self.assertNotEqual(first.slug, second.slug)
        self.assertFalse(first.slug.endswith("-"))

    def test_editing_the_title_keeps_the_slug(self):
        project = make_project("First Name")
        project.title = "Second Name"
        project.save()
        project.refresh_from_db()
        self.assertEqual(project.slug, "first-name")

    def test_a_row_without_a_slug_still_works_and_gets_one_on_first_visit(self):
        # After a code rollback the previous release can insert a project; the database default
        # leaves its slug empty. The site must not break on it once the new code is back.
        project = make_project("Made By The Old Release")
        Project.objects.filter(pk=project.pk).update(slug="")
        project.refresh_from_db()
        self.assertEqual(project.get_absolute_url(), f"/project/{project.pk}/")
        self.assertEqual(self.client.get(reverse("portfolio")).status_code, 200)
        response = self.client.get(f"/project/{project.pk}/")
        self.assertRedirects(response, "/project/made-by-the-old-release/", status_code=301)

    def test_a_slug_chosen_by_hand_is_kept(self):
        self.assertEqual(make_project("Anything", slug="my-own").slug, "my-own")


class ProjectVisibilityTests(SmokeTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shown = make_project("Shown Project")
        cls.hidden = make_project("Hidden Project", is_published=False)

    def test_new_projects_are_published_and_not_featured(self):
        self.assertTrue(self.shown.is_published)
        self.assertFalse(self.shown.is_featured)

    def test_unpublished_project_is_absent_from_the_home_page(self):
        page = self.client.get(reverse("portfolio")).content.decode()
        self.assertIn("Shown Project", page)
        self.assertNotIn("Hidden Project", page)

    def test_unpublished_project_page_and_old_id_link_are_404(self):
        self.assertEqual(self.client.get(self.hidden.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(f"/project/{self.hidden.pk}/").status_code, 404)


class ProjectContentTests(SmokeTestCase):
    def test_summary_falls_back_to_github_description_then_subtitle(self):
        project = make_project(subtitle="Sub", summary="Sum", github_description="Hub")
        self.assertEqual(project.display_summary, "Sum")
        project.summary = ""
        self.assertEqual(project.display_summary, "Hub")
        project.github_description = ""
        self.assertEqual(project.display_summary, "Sub")
        project.subtitle = ""
        self.assertEqual(project.display_summary, "")

    def test_project_without_image_or_write_up_renders(self):
        # What the GitHub sync creates: a title and little else.
        project = Project.objects.create(title="Bare Project", github_description="From GitHub <b>escaped</b>")
        home = self.client.get(reverse("portfolio"))
        self.assertEqual(home.status_code, 200)
        self.assertContains(home, "Bare Project")
        self.assertContains(home, "From GitHub &lt;b&gt;escaped&lt;/b&gt;")
        page = self.client.get(project.get_absolute_url())
        self.assertEqual(page.status_code, 200)
        self.assertNotContains(page, "<img")
        self.assertNotContains(page, "About the Project")

    def test_projects_without_a_repository_do_not_collide(self):
        first = make_project("One", github_repo="")
        second = make_project("Two")
        first.refresh_from_db()
        self.assertIsNone(first.github_repo)
        self.assertIsNone(second.github_repo)

    def test_two_projects_cannot_share_a_repository(self):
        make_project("One", github_repo="Arbelaezch/callback")
        with self.assertRaises(IntegrityError), transaction.atomic():
            make_project("Two", github_repo="Arbelaezch/callback")


class ProjectAdminTests(SmokeTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser("admin", "admin@example.com", "pw-for-tests")

    def post_new_project(self, **data):
        form = {
            "title": "Same Title", "slug": "", "subtitle": "", "summary": "", "category": "", "primary_language": "",
            "timeline": "", "is_published": "on", "order": "0", "description": "", "lessons_learned": "",
            "project_url": "", "github_url": "", "github_repo": "",
        }
        form.update(data)
        return self.client.post(reverse("admin:portfolio_project_add"), form)

    def test_adding_two_projects_with_the_same_title_works(self):
        # The same mistake made recipes and movies answer 500 (issue #88).
        self.client.force_login(self.admin)
        for _ in range(2):
            self.assertRedirects(self.post_new_project(), reverse("admin:portfolio_project_changelist"))
        self.assertEqual(
            sorted(Project.objects.values_list("slug", flat=True)), ["same-title", "same-title-2"])

    def test_flags_can_be_edited_in_the_list_and_sync_fields_are_read_only(self):
        self.client.force_login(self.admin)
        project = make_project(github_description="Synced text")
        changelist = self.client.get(reverse("admin:portfolio_project_changelist"))
        self.assertContains(changelist, 'name="form-0-is_featured"')
        form_page = self.client.get(reverse("admin:portfolio_project_change", args=[project.pk]))
        self.assertContains(form_page, "Synced text")
        self.assertNotContains(form_page, 'name="github_description"')


class ProjectSlugMigrationTests(TransactionTestCase):
    """0004 fills slugs for the rows that existed before the column did, then 0005 makes it unique."""

    before = [("portfolio", "0003_project_publishing_and_github_fields")]
    after = [("portfolio", "0005_project_slug_unique")]

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())

    def test_existing_projects_get_unique_slugs(self):
        executor = MigrationExecutor(connection)
        executor.migrate(self.before)
        OldProject = executor.loader.project_state(self.before).apps.get_model("portfolio", "Project")
        for title in ["Family Food", "Family Food", "???", "1984", "Kept"]:
            OldProject.objects.create(title=title, subtitle="s", description="<p>d</p>")
        OldProject.objects.filter(title="Kept").update(slug="already-set")

        executor = MigrationExecutor(connection)
        executor.migrate(self.after)
        NewProject = executor.loader.project_state(self.after).apps.get_model("portfolio", "Project")
        slugs = list(NewProject.objects.order_by("pk").values_list("slug", flat=True))
        self.assertEqual(slugs, ["family-food", "family-food-2", "project", "project-1984", "already-set"])
