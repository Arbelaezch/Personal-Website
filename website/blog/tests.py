from blog.models import Article
from website.testing import SmokeTestCase


class BlogRetiredTests(SmokeTestCase):
    def test_blog_pages_are_gone(self):
        Article.objects.create(title="Hello", subtitle="First post", body="<p>Body text</p>", subject="META")
        for url in ["/blog/", "/blog/blog/1"]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_no_public_page_links_to_the_blog(self):
        self.assertNotContains(self.client.get("/"), "/blog/")


class ArticleModelTests(SmokeTestCase):
    """The model stays for one release (see blog/admin.py)."""

    def test_newest_first_and_formatted_date(self):
        first = Article.objects.create(title="First", body="<p>1</p>", subject="Film")
        second = Article.objects.create(title="Second", body="<p>2</p>", subject="Music")
        self.assertEqual(list(Article.get_reverse_chronological_order()), [second, first])
        self.assertRegex(first.get_formatted_date(), r"^\d{2} [A-Z][a-z]+ \d{4}$")
        self.assertEqual(str(first), "First")
