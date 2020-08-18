from django.urls import path

from . import views

urlpatterns = [
    path("logs/", views.logs),
    path("clubs/new/", views.clubs_new),
    path("clubs/edit/<str:id>/", views.clubs_edit),
    path("clubs/delete/<str:id>/", views.clubs_delete),
    path("coordinators/new/", views.coordinators_new),
    path("coordinators/edit/<str:id>/", views.coordinators_edit),
    # path("coordinators/delete/<str:id>/", views.coordinators_edit),
]
