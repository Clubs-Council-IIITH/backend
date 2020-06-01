from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EventSerializer
from base.models import Event

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


class EventView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        token = self.request.headers.get("Authorization")[6:]
        user = Token.objects.get(key=token).user
        queryset = Event.objects.filter(user=user)
