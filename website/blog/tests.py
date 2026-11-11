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
