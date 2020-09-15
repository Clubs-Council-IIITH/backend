from django.urls import path

from . import views

urlpatterns = [
    path("logs/", views.logs),
    path("clubs/", views.clubs),
    path("clubs/new/", views.clubs_new),
    path("clubs/edit/<str:id>/", views.clubs_edit),
    path("clubs/delete/<str:id>/", views.clubs_delete),
    path("events/", views.events),
    path("events/new/", views.events_new),
    path("events/edit/<str:id>/", views.events_edit),
    path("events/delete/<str:id>/", views.events_delete),
    path("coordinators/", views.coordinators),
    path("coordinators/new/", views.coordinators_new),
    path("coordinators/edit/<str:id>/", views.coordinators_edit),
]
