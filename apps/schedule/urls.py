from django.urls import path
from apps.schedule import views

urlpatterns = [

    #  schedule
    path('schedule/add/', views.add_schedule, name='schedules'),
    path('schedule/<int:nid>/edit/', views.edit_schedule, name='schedules'),
    path('schedules/', views.schedules, name='schedules'),

    #  schedule filtered by user
    path('my_schedules/', views.my_schedules, name='schedules'),

    #  record
    path('records/', views.records, name='records'),

    #  record filtered by user
    path('my_records/', views.my_record, name='records'),

]
