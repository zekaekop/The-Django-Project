from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class HomeAnonymousUserTests(TestCase):
    """
    Anonymous users should be redirected or blocked
    """

    def test_home_redirects_for_anonymous(self):
        response = self.client.get(reverse("home:home"))
        self.assertEqual(response.status_code, 302)

    def test_top_day_redirects_for_anonymous(self):
        response = self.client.get(reverse("home:top_day"))
        self.assertEqual(response.status_code, 302)

    def test_top_month_redirects_for_anonymous(self):
        response = self.client.get(reverse("home:top_month"))
        self.assertEqual(response.status_code, 302)

    def test_upvote_404_for_anonymous(self):
        response = self.client.get(
            reverse("home:upvote_post", kwargs={"id": 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_home_404_for_anonymous(self):
        response = self.client.get(
            reverse("home:delete_home", kwargs={"id": 1})
        )
        self.assertEqual(response.status_code, 404)


class HomeAuthenticatedUserTests(TestCase):
    """
    Authenticated users should access home views
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_home_loads_for_authenticated(self):
        response = self.client.get(reverse("home:home"))
        self.assertEqual(response.status_code, 200)

    def test_top_day_loads_for_authenticated(self):
        response = self.client.get(reverse("home:top_day"))
        self.assertEqual(response.status_code, 200)

    def test_top_month_loads_for_authenticated(self):
        response = self.client.get(reverse("home:top_month"))
        self.assertEqual(response.status_code, 200)

    def test_upvote_safe_for_authenticated(self):
        response = self.client.get(
            reverse("home:upvote_post", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [302, 404])

    def test_delete_home_safe_for_authenticated(self):
        response = self.client.get(
            reverse("home:delete_home", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [302, 404])
