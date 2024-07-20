# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, add_users, add_admin, logout
from django.contrib.auth.views import LogoutView
from apps.households import views as households

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout, name="logout"),

    # add user and admin
    path('add_users/', add_users, name="add-users"),
    path('add_admin/', add_admin, name="add-admin"),
]
