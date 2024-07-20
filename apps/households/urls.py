# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.households import views

urlpatterns = [

    #  barangay
    path('barangay/add/', views.add_barangay, name='households'),
    path('barangay/<int:nid>/view/', views.edit_barangay, name='households'),
    path('barangay/', views.barangay, name='households'),
    path('<name>/view/', views.barangayByName, name='households'),
    path('barangay/export_to_csv/', views.csv_barangay, name='households'),
    # path('<name>/export_to_csv/', views.csv_barangayByName, name='households'),
    path('barangay/<int:nid>/export_to_word/', views.word_barangay, name='households'),

    #  household
    path('households/export_to_csv/', views.csv_household, name='households'),
    path('add_households/', views.add_households, name="households"),
    path('households/', views.households, name='households'),
    path('household/<int:nid>/view/', views.view_household, name='households'),
    path('household/<int:nid>/edit/', views.edit_households, name='households'),
    path('household/approval/list/', views.approval_householdList, name='approvals'),
    path('household/bulk-approval/', views.bulkapprove_household, name='approvals'),
    path('household/<int:nid>/approval/view/', views.approve_household, name='approvals'),

    path('household/lumon/<int:nid>/view/', views.view_householdLumon, name='households'),
    path('household/<int:nid>/export/', views.export_household, name='households'),

    #  lumon
    path('add_lumon/', views.add_lumon, name="households"),
    path('household/lumon/<int:nid>/edit/', views.edit_lumon, name='households'),
    path('lumon/', views.lumon, name='households'),
    path('lumon/<int:nid>/export/', views.export_lumon, name='households'),
    path('lumon/export_to_csv/', views.csv_lumon, name='households'),

    path('household/lumon/bulk-approval/', views.bulkapprove_lumon, name='approvals'),
    path('household/lumon/approval/list/', views.approval_lumonList, name='approvals'),
    path('household/lumon/<int:nid>/approval/view/', views.approve_lumon, name='approvals'),

]
