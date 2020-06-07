from django.urls import path
from . import views

urlpatterns = [
    path("logs/", views.logs),
    path("clubs/", views.clubs),
    path("clubs/new/", views.clubs_new),
    path("clubs/edit/<str:id>", views.clubs_edit),
]
