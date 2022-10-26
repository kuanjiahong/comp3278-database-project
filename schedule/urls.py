from django.urls import path
from django.views.generic import RedirectView
from schedule import views

app_name = 'schedule'
urlpatterns = [
    path("login", views.login_mainpage, name="login"),
    path("home", views.home_page, name="home"),
    path("logs", views.view_logs, name="logs"),
    path("", RedirectView.as_view(url='/schedule/login'), name='go-to-login'),
]