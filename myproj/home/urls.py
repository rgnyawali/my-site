from django.urls import path, include
from . import views

app_name="home"
urlpatterns = [
    path('', views.HomeView.as_view(), name="homepage"),
    path('register/',views.register_user, name="register"),
    # path("accounts/", include("django.contrib.auth.urls")),
    path('password-reset/',views.password_reset, name="password-reset"),
    path('set-password/',views.set_password, name="set-password"),

    ]
