# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, logout_view
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout_view, name="logout"),
    path("forgot_password/", views.forgot_password_view, name="forgot_password"),
    path("reset_password/", views.reset_password_view, name="reset_password"),
    path("account-management/", views.account_management, name="account_management"),
    path("account-management/<int:user_id>/status/", views.set_account_status, name="set_account_status"),
    path("account-management/<int:user_id>/role/", views.set_account_role, name="set_account_role"),
    path("account-management/<int:user_id>/delete/", views.delete_account, name="delete_account"),
]

