from django.urls import path

from . import views

urlpatterns = [
    path("all-categories/<slug:level>", views.categories, name="all_categories"),
    path("play/<slug:level>/<int:cat>", views.quiz_view, name="game"),
    path("results", views.resulting, name="result"),
    path("results/<slug:category>", views.resulting, name="result_category"),
    path("r", views.random, name="random"),
    path("playing/<slug:category>", views.play_users, name="gaming"),
    path("users-questions", views.users_q, name="users_section"),
    path("add-questions/<slug:category>", views.add_q, name="add_questions"),
]