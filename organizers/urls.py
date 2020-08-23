from django.urls import path

from . import views

urlpatterns = [
    path("events/new/", views.events_new),
    path("events/edit/<str:id>/", views.events_edit),
    path("events/delete/<str:id>/", views.events_delete),
    path("budget/proposals/", views.proposals),
    path("budget/proposals/new/", views.proposals_new),
]
