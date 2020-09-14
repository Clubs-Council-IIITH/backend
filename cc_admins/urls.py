from django.urls import path

from . import views

urlpatterns = [
    path("logs/", views.logs),
    path("clubs/new/", views.clubs_new),
    path("clubs/edit/<str:id>/", views.clubs_edit),
    path("clubs/delete/<str:id>/", views.clubs_delete),
    path("coordinators/new/", views.coordinators_new),
    path("coordinators/edit/<str:id>/", views.coordinators_edit),
    path("updates/new/", views.updates_new),
    path("updates/edit/<str:id>/", views.updates_edit),
    path("updates/delete/<str:id>/", views.updates_delete),
    # path("coordinators/delete/<str:id>/", views.coordinators_edit),
]
