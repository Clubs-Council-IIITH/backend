from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cc_admins.serializers import ClubSerializer
from organizers.serializers import EventSerializer
from .models import Club, Event
from django.utils import timezone

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response


@login_required
def get_token(request):
    user = request.user
    usergroup = "enduser"
    if user.groups.exists():
        usergroup = user.groups.all()[0].name
    token, created = Token.objects.get_or_create(user=user)
    context = {"token": token.key, "usergroup": usergroup}
    return render(request, "login_redirect.html", context)


@api_view(["GET"])
def events(request):
    events = Event.objects.all()
    for event in events:
        if event.datetime < timezone.now() and event.state != "deleted":
            event.state = "completed"
            event.save()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def clubs(request):
    clubs = Club.objects.all()
    serializer = ClubSerializer(clubs, many=True)
    return Response(serializer.data)
