from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EventSerializer
from base.models import Event


class EventView(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
