from django.urls import path

from . import views

urlpatterns = [
    path("token/", views.get_token),
    path("session/", views.get_session),
    path("endsession/", views.end_session),
    path("updates/", views.updates),
    path("updates/new/", views.updates_new),
    path("updates/edit/<str:id>/", views.updates_edit),
    path("updates/delete/<str:id>/", views.updates_delete),
]
