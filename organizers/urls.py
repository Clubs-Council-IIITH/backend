from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.events),
    path("events/new/", views.events_new),
    path("events/edit/<str:id>", views.events_edit),
    path("events/delete/<str:id>", views.events_delete),
]
