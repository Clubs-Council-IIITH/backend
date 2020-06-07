from django.urls import path
from . import views

urlpatterns = [
    path("logs/", views.logs),
    path("clubs/", views.clubs),
]
