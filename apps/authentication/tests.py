# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase
from django.urls import reverse


class AccountManagementTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin", password="admin-password", is_staff=True
        )
        self.user = User.objects.create_user(
            username="ordinary", password="user-password"
        )

    def test_ordinary_user_cannot_open_account_management(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("account_management"))

        self.assertEqual(response.status_code, 403)

    def test_admin_can_open_account_management(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("account_management"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ordinary")

    def test_admin_can_revoke_and_restore_registration(self):
        self.client.force_login(self.admin)
        status_url = reverse("set_account_status", args=[self.user.id])

        self.client.post(status_url, {"action": "deactivate"})
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        self.client.post(status_url, {"action": "activate"})
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_admin_can_delete_an_ordinary_account(self):
        self.client.force_login(self.admin)

        self.client.post(reverse("delete_account", args=[self.user.id]))

        self.assertFalse(User.objects.filter(pk=self.user.id).exists())

    def test_admin_cannot_delete_own_account(self):
        self.client.force_login(self.admin)

        self.client.post(reverse("delete_account", args=[self.admin.id]))

        self.assertTrue(User.objects.filter(pk=self.admin.id).exists())

    def test_superuser_account_is_protected(self):
        superuser = User.objects.create_superuser(
            username="root", password="root-password", email="root@example.com"
        )
        self.client.force_login(self.admin)

        self.client.post(reverse("delete_account", args=[superuser.id]))
        self.client.post(
            reverse("set_account_status", args=[superuser.id]),
            {"action": "deactivate"},
        )

        superuser.refresh_from_db()
        self.assertTrue(superuser.is_active)

    def test_account_actions_require_post(self):
        self.client.force_login(self.admin)

        delete_response = self.client.get(
            reverse("delete_account", args=[self.user.id])
        )
        status_response = self.client.get(
            reverse("set_account_status", args=[self.user.id])
        )

        self.assertEqual(delete_response.status_code, 405)
        self.assertEqual(status_response.status_code, 405)

    def test_sidebar_does_not_show_account_or_administration_sections(self):
        request = RequestFactory().get("/")
        request.user = self.admin

        html = render_to_string("includes/sidenav.html", request=request)

        self.assertNotIn("Account Management", html)
        self.assertNotIn("Register User", html)
        self.assertNotIn("ARSP website", html)
        self.assertNotIn("Logout", html)

    def test_profile_dropdown_shows_administration_and_account_options_to_admins(self):
        request = RequestFactory().get("/")
        request.user = self.admin

        html = render_to_string("includes/navigation.html", request=request)

        self.assertIn('id="user-menu-toggle"', html)
        self.assertIn("Administration", html)
        self.assertIn("Account Management", html)
        self.assertIn("Register User", html)
        self.assertIn("Account", html)
        self.assertIn("ARSP website", html)
        self.assertIn("Logout", html)

    def test_profile_dropdown_hides_administration_options_from_ordinary_users(self):
        request = RequestFactory().get("/")
        request.user = self.user

        html = render_to_string("includes/navigation.html", request=request)

        self.assertNotIn("Account Management", html)
        self.assertNotIn("Register User", html)
        self.assertIn("ARSP website", html)
        self.assertIn("Logout", html)

    def test_profile_dropdown_keeps_legacy_avatar(self):
        request = RequestFactory().get("/")
        request.user = self.user

        html = render_to_string("includes/navigation.html", request=request)

        self.assertIn('/static/assets/img/theme/Bacteria2.gif', html)
        self.assertIn('class="avatar avatar-sm rounded-circle"', html)

    def test_profile_dropdown_uses_legacy_bootstrap_structure(self):
        request = RequestFactory().get("/")
        request.user = self.user

        html = render_to_string("includes/navigation.html", request=request)

        self.assertIn('<li class="nav-item dropdown">', html)
        self.assertIn('id="user-menu-toggle"', html)
        self.assertIn('data-toggle="dropdown"', html)
        self.assertNotIn('<details', html)

    def test_sidebar_keeps_legacy_white_argon_shell(self):
        request = RequestFactory().get("/")
        request.user = self.user

        html = render_to_string("includes/sidenav.html", request=request)

        self.assertIn("navbar-light bg-white", html)
        self.assertIn("/static/assets/img/brand/egasp_n.png", html)
        self.assertNotIn('class="nav-section"', html)

    def test_restricted_table_controls_are_disabled_for_ordinary_users(self):
        request = RequestFactory().get("/show/")
        request.user = self.user

        html = render_to_string("home/tables.html", request=request)

        self.assertIn("Antibiotic Results", html)
        self.assertIn('id="antibiotic-results-button"', html)
        self.assertIn('id="delete-all-button"', html)
        self.assertIn('aria-disabled="true"', html)
        self.assertNotIn('href="/test_results-view/"', html)
        self.assertNotIn("data-target=\"#deleteAllModal\"", html)

    def test_restricted_table_controls_are_enabled_for_admins(self):
        request = RequestFactory().get("/show/")
        request.user = self.admin

        html = render_to_string("home/tables.html", request=request)

        self.assertIn('href="/test_results-view/"', html)
        self.assertIn('data-target="#deleteAllModal"', html)
        self.assertNotIn('aria-disabled="true"', html)

    def test_antibiotic_results_is_admin_only(self):
        self.client.force_login(self.user)
        forbidden_response = self.client.get(reverse("abxentry_view"))
        self.assertEqual(forbidden_response.status_code, 403)

        self.client.force_login(self.admin)
        allowed_response = self.client.get(reverse("abxentry_view"))
        self.assertEqual(allowed_response.status_code, 200)

    def test_delete_all_is_admin_only_and_post_only(self):
        self.client.force_login(self.user)
        forbidden_response = self.client.post(reverse("delete_all_egasp"))
        self.assertEqual(forbidden_response.status_code, 403)

        self.client.force_login(self.admin)
        method_response = self.client.get(reverse("delete_all_egasp"))
        self.assertEqual(method_response.status_code, 405)

    def test_superuser_can_promote_and_demote_an_account(self):
        superuser = User.objects.create_superuser(
            username="root", password="root-password", email="root@example.com"
        )
        self.client.force_login(superuser)
        role_url = f"/account-management/{self.user.id}/role/"

        self.client.post(role_url, {"role": "staff"})
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

        self.client.post(role_url, {"role": "user"})
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_staff_account_cannot_assign_roles(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            f"/account-management/{self.user.id}/role/",
            {"role": "staff"},
        )

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.user.is_staff)

    def test_superuser_role_is_protected(self):
        superuser = User.objects.create_superuser(
            username="root", password="root-password", email="root@example.com"
        )
        self.client.force_login(superuser)

        self.client.post(
            f"/account-management/{superuser.id}/role/",
            {"role": "user"},
        )

        superuser.refresh_from_db()
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_role_assignment_requires_post(self):
        superuser = User.objects.create_superuser(
            username="root", password="root-password", email="root@example.com"
        )
        self.client.force_login(superuser)

        response = self.client.get(
            f"/account-management/{self.user.id}/role/"
        )

        self.assertEqual(response.status_code, 405)

    def test_superuser_sees_role_controls_and_django_admin_link(self):
        superuser = User.objects.create_superuser(
            username="root", password="root-password", email="root@example.com"
        )
        self.client.force_login(superuser)

        response = self.client.get(reverse("account_management"))

        self.assertContains(response, "Django Admin")
        self.assertContains(response, reverse("admin:index"))
        self.assertContains(
            response,
            f"/account-management/{self.user.id}/role/",
        )

    def test_staff_account_does_not_see_role_controls_or_django_admin_link(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("account_management"))

        self.assertNotContains(response, "Django Admin")
        self.assertNotContains(
            response,
            f"/account-management/{self.user.id}/role/",
        )


class ForgotPasswordTests(TestCase):
    def test_unique_email_starts_password_reset_for_matching_account(self):
        user = User.objects.create_user(
            username="unique-user",
            email="unique@example.com",
            password="old-password",
        )

        response = self.client.post(
            reverse("forgot_password"),
            {"username_or_email": "unique@example.com"},
        )

        self.assertRedirects(response, reverse("reset_password"))
        self.assertEqual(self.client.session["reset_user_id"], user.id)

    def test_shared_email_requires_username_instead_of_selecting_an_account(self):
        User.objects.create_user(
            username="shared-one",
            email="shared@example.com",
            password="old-password",
        )
        User.objects.create_user(
            username="shared-two",
            email="shared@example.com",
            password="old-password",
        )

        response = self.client.post(
            reverse("forgot_password"),
            {"username_or_email": "shared@example.com"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("reset_user_id", self.client.session)
        self.assertContains(
            response,
            "Multiple accounts use this email. Enter your username instead.",
        )

    def test_username_still_starts_password_reset_when_emails_are_shared(self):
        selected_user = User.objects.create_user(
            username="shared-one",
            email="shared@example.com",
            password="old-password",
        )
        User.objects.create_user(
            username="shared-two",
            email="shared@example.com",
            password="old-password",
        )

        response = self.client.post(
            reverse("forgot_password"),
            {"username_or_email": "shared-one"},
        )

        self.assertRedirects(response, reverse("reset_password"))
        self.assertEqual(self.client.session["reset_user_id"], selected_user.id)


class ResetPasswordPageTests(TestCase):
    def test_each_password_field_has_its_own_non_submit_visibility_control(self):
        user = User.objects.create_user(
            username="reset-user",
            email="reset@example.com",
            password="old-password",
        )
        session = self.client.session
        session["reset_user_id"] = user.id
        session.save()

        response = self.client.get(reverse("reset_password"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'class="input-group-text toggle-pw"',
            count=2,
        )
        self.assertContains(response, 'data-password-target="id_password1"')
        self.assertContains(response, 'data-password-target="id_password2"')
        self.assertContains(response, 'aria-pressed="false"', count=2)
