from django.urls import reverse

from portfolio.models import Project
from website.testing import SmokeTestCase, tiny_image


class PortfolioPagesTests(SmokeTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            title="Callback", subtitle="Resume tailoring", description="<p>Writes resumes.</p>",
            lessons_learned="Ship small.", image=tiny_image(), order=1,
        )

    def test_home_lists_projects(self):
        response = self.client.get(reverse("portfolio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Callback")

    def test_project_detail(self):
        response = self.client.get(reverse("project_detail", kwargs={"pk": self.project.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Callback")

    def test_unknown_project_is_404(self):
        self.assertEqual(self.client.get(reverse("project_detail", kwargs={"pk": 9999})).status_code, 404)


class ProjectOrderingTests(SmokeTestCase):
    def test_home_lists_the_highest_order_first_and_str_is_the_title(self):
        low = Project.objects.create(title="LowOrder", subtitle="s", description="<p>d</p>", image=tiny_image(), order=1)
        high = Project.objects.create(title="HighOrder", subtitle="s", description="<p>d</p>", image=tiny_image(), order=9)
        page = self.client.get(reverse("portfolio")).content.decode()
        self.assertLess(page.index("HighOrder"), page.index("LowOrder"))
        self.assertEqual(str(low), "LowOrder")
        self.assertEqual(str(high), "HighOrder")
