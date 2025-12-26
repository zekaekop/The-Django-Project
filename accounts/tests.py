from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsUrlTests(TestCase):

    def test_login_page_for_anonymous_user(self):
        """
        Anonymous user should see login form
        """
        response = self.client.get("/accounts/login/")    #Inside of this you can Use ->   response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_redirect_for_authenticated_user(self):
        """
        Authenticated user should be redirected from login page
        """
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 302)

    def test_signin_page_loads(self):
        """
        Signin page should load for GET request
        """
        response = self.client.get("/accounts/signin/")
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects(self):
        """
        Logout always redirects to login page
        """
        response = self.client.get("/accounts/logout/")
        self.assertEqual(response.status_code, 302)
