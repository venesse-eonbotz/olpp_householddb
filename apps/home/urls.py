# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='dashboard'),
    path('dashboard/', views.index, name='dashboard'),
    path('dashboard/stats-all/', views.indexAll, name='dashboard-all'),

    path('admin/', views.admin, name='admin'),
    path('admin/<int:nid>/view/', views.admin_view, name='admin-view'),

    path('users/', views.users, name='users-access'),
    path('user/<int:nid>/view/', views.user_view, name='user-view'),
    path('user/<int:nid>/deactivate/', views.deactivate_user, name='deactivate_user'),
    path('user/<int:nid>/activate/', views.activate_user, name='activate_user'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
