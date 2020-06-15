from django.urls import path
from . import views

urlpatterns = [
    path("clubs/", views.clubs),
    path("events/", views.events),
]
