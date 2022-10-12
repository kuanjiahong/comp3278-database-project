from django.urls import path
from schedule import views

urlpatterns = [
    path("hello", views.hello),
    path("logs", views.view_logs, name="logs"),
    path("timetable", views.view_personal_timetable, name="timetable")
]