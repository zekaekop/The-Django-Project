from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AdminPanelAnonymousTests(TestCase):
    """
    Anonymous users should NOT access admin panel URLs
    """

    def test_admin_panel_default_404(self):
        response = self.client.get(reverse("admin_panel:admin_panel"))
        self.assertEqual(response.status_code, 404)

    def test_admin_panel_users_404(self):
        response = self.client.get(reverse("admin_panel:admin_panel_users"))
        self.assertEqual(response.status_code, 404)

    def test_admin_panel_posts_404(self):
        response = self.client.get(reverse("admin_panel:admin_panel_posts"))
        self.assertEqual(response.status_code, 404)

    def test_admin_panel_contacts_404(self):
        response = self.client.get(reverse("admin_panel:admin_panel_contact"))
        self.assertEqual(response.status_code, 404)


class AdminPanelStaffTests(TestCase):
    """
    Staff users should access admin panel pages
    """

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="testpass123",
            is_staff=True
        )
        self.client.login(username="staffuser", password="testpass123")

    def test_admin_panel_default_page(self):
        response = self.client.get(reverse("admin_panel:admin_panel"))
        self.assertEqual(response.status_code, 200)

    def test_admin_panel_users_page(self):
        response = self.client.get(reverse("admin_panel:admin_panel_users"))
        self.assertEqual(response.status_code, 200)

    def test_admin_panel_posts_page(self):
        response = self.client.get(reverse("admin_panel:admin_panel_posts"))
        self.assertEqual(response.status_code, 200)

    def test_admin_panel_contacts_page(self):
        response = self.client.get(reverse("admin_panel:admin_panel_contact"))
        self.assertEqual(response.status_code, 200)


class AdminPanelActionUrlTests(TestCase):
    """
    Action URLs should redirect or 404 safely
    """

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staffaction",
            password="testpass123",
            is_staff=True,
            is_superuser=True
        )
        self.client.login(username="staffaction", password="testpass123")

    def test_delete_post_adminpanel_url(self):
        response = self.client.get(
            reverse("admin_panel:delete_post_adminpanel", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [302, 404])

    def test_delete_contact_adminpanel_url(self):
        response = self.client.get(
            reverse("admin_panel:delete_contact_adminpanel", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [302, 404])

    def test_modify_contact_adminpanel_url(self):
        response = self.client.get(
            reverse("admin_panel:modify_contact_adminpanel", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [200, 302, 404])

    def test_set_user_staff_perm_url(self):
        response = self.client.get(
            reverse("admin_panel:set_user_perms_staff_adminpanel", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [302, 404])

    def test_set_user_superuser_perm_url(self):
        response = self.client.get(
            reverse("admin_panel:set_user_perms_superuser_adminpanel", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [302, 404])

    def test_active_state_user_account_url(self):
        response = self.client.get(
            reverse("admin_panel:active_state_user_account", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [302, 404])

    def test_password_change_user_account_url(self):
        response = self.client.get(
            reverse("admin_panel:password_change_user_account", kwargs={"id": 1})
        )
        self.assertIn(response.status_code, [200, 302, 404])







"""Check the Model's"""

class ModelTestCase(TestCase):

    def setUp(self):
        print("SetUp Called !")
        self.user = User.objects.create_user(
            username = "testuser",
            email = "testuser@example.com",
            password = "testpass123"
        )



    def test_account_email(self):
        """
        Check that the user's email is saved correctly
        """
        self.assertEqual(self.user.email, "testuser@example.com")