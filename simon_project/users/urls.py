from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signin", views.signin_view, name="signin"),
    path("profile", views.profile_view, name="profile"),
]
