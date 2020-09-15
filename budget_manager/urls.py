from django.urls import path

from . import views

urlpatterns = [
    path("budget/proposals/", views.proposals),
    path("budget/proposals/new/", views.proposals_new),
]
