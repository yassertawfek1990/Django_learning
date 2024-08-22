from django.urls import path

from . import views

urlpatterns = [
    path("<slug:name>", views.get_data, name="api_view"),
    path("add/<slug:name>", views.add_data, name="adding"),
]