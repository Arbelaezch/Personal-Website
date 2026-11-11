from django.urls import reverse

from blog.models import Article
from website.testing import SmokeTestCase


class BlogPagesTests(SmokeTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article = Article.objects.create(
            title="Hello", subtitle="First post", body="<p>Body text</p>", subject="META",
        )

    def test_blog_index_lists_articles(self):
        response = self.client.get(reverse("BlogView"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello")

    def test_article_page_renders(self):
        response = self.client.get(reverse("ArticleView", kwargs={"article_id": self.article.pk}))
        self.assertEqual(response.status_code, 200)


class ArticleModelTests(SmokeTestCase):
    def test_newest_first_and_formatted_date(self):
        first = Article.objects.create(title="First", body="<p>1</p>", subject="Film")
        second = Article.objects.create(title="Second", body="<p>2</p>", subject="Music")
        self.assertEqual(list(Article.get_reverse_chronological_order()), [second, first])
        self.assertRegex(first.get_formatted_date(), r"^\d{2} [A-Z][a-z]+ \d{4}$")
        self.assertEqual(str(first), "First")
