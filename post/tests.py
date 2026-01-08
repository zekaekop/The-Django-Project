from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class InfoViewTests(TestCase):

    def test_about_page_loads(self):
        response = self.client.get(reverse("info:about"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        response = self.client.get(reverse("info:contact"))
        self.assertEqual(response.status_code, 200)




from django.contrib.auth.models import User

class PostIndexTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_post_index_page_loads(self):
        response = self.client.get(reverse("post:index"))
        self.assertEqual(response.status_code, 200)



class PostDetailTests(TestCase):

    def test_post_detail_safe(self):
        response = self.client.get(
            reverse("post:detail", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [200, 404])


class PostCreateTests(TestCase):

    def test_create_post_requires_login(self):
        response = self.client.get(reverse("post:create"))
        self.assertEqual(response.status_code, 404)




class PostActionSecurityTests(TestCase):

    def test_upvote_requires_login(self):
        response = self.client.get(
            reverse("post:upvote_post", kwargs={"id": 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_report_requires_login(self):
        response = self.client.get(
            reverse("post:report", kwargs={"id": 1})
        )
        self.assertEqual(response.status_code, 404)








class PostAuthenticatedTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_create_post_authenticated(self):
        response = self.client.get(reverse("post:create"))
        self.assertEqual(response.status_code, 200)

    def test_upvote_authenticated_safe(self):
        response = self.client.get(
            reverse("post:upvote_post", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [302, 404])
