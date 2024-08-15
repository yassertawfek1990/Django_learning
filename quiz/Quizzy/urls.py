from django.urls import path

from . import views

urlpatterns = [
    path("all-categories/<slug:level>", views.categories, name="all_categories"),
    path("play/<slug:level>/<int:cat>", views.quiz_view, name="game"),
    path("results", views.resulting, name="result"),
    path("r", views.random, name="random"),
]