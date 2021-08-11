from django.urls import path
from django_cas_ng.views import LoginView, LogoutView
from authentication.views import jwt

urlpatterns = [
    path("accounts/jwt", jwt),
    path("accounts/login", LoginView.as_view(), name="cas_ng_login"),
    path("accounts/logout", LogoutView.as_view(), name="cas_ng_logout"),
]
