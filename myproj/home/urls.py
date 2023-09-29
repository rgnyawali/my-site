from django.urls import path, include
from . import views

app_name="home"
urlpatterns = [
    path('', views.HomeView.as_view(), name="homepage"),
    path('register/',views.register_user, name="register"),

    ]
