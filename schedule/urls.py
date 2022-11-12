from django.urls import path
from django.views.generic import RedirectView
from schedule import views

app_name = 'schedule'
urlpatterns = [
    path("login", views.login_mainpage, name="login"),
    path("logout", views.logout_mainpage, name="logout"),
    path("home", views.home_page, name="home"),
    path("send_to_email", views.send_upcoming_classes, name="send-to-email"),
    path("logs", views.view_logs, name="logs"),
    path("", RedirectView.as_view(url='/schedule/login'), name='go-to-login'),
]