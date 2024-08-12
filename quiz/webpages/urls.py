from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="main"),
    path("contact-us", views.contact_us, name="contact"),
    path("about-us", views.about_us, name="about"),
    path("suggestion", views.suggestion, name="suggestion")
]