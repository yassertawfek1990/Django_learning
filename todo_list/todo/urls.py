from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_tasks,name="tasks"),
    path("add",views.adding,name="add"),
    path("user", views.print_user, name = "printuser")
]