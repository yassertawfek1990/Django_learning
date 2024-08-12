from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/register/", views.register_user, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate")
]