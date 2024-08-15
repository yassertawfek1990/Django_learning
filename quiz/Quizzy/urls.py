from django.urls import path

from . import views

urlpatterns = [
    path("all-categories", views.categories, name="all_categories"),
    path("play", views.quiz_view, name="game"),
    path("results", views.resulting, name="result"),
]