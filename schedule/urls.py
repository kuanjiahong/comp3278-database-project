from django.urls import path
from schedule import views

app_name = 'schedule'
urlpatterns = [
    path("hello", views.hello),
    path("home", views.home_page, name="home"),
    path("logs", views.view_logs, name="logs"),
]