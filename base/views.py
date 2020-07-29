from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Club, Event, Coordinator
from cc_admins.serializers import ClubSerializer, CoordinatorSerializer
from organizers.serializers import EventSerializer
from django.utils import timezone
from django.http import JsonResponse

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Authentication
@login_required
def get_token(request):
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    context = {"token": token.key}
    return render(request, "login_redirect.html", context)


@api_view(["GET"])
def get_session(request):
    session = {"usergroup": None, "is_authenticated": False}
    if not request.user.is_anonymous:
        try:
            session["usergroup"] = str(request.user.groups.all()[0])
        except:
            pass
        session["is_authenticated"] = True
    return JsonResponse(session)


# Events R
@api_view(["GET"])
def events(request):
    event_id = request.query_params.get("id", None)
    token = request.headers.get("Authorization", None)
    events = Event.objects.all()
    for event in events:
        if event.datetime < timezone.now() and event.state != "deleted":
            event.state = "completed"
            event.save()
    if token:
        mail = Token.objects.get(key=token[6:]).user
        club = Club.objects.filter(mail=mail).first()
        if club:
            events = events.filter(club=club)
    if event_id is not None:
        events = events.filter(id=event_id)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


# Clubs R
@api_view(["GET"])
def clubs(request):
    club_id = request.query_params.get("id", None)
    clubs = Club.objects.all()
    if club_id is not None:
        clubs = clubs.filter(id=club_id)
    serializer = ClubSerializer(clubs, many=True)
    return Response(serializer.data)


# Coordinators R
@api_view(["GET"])
def coordinators(request):
    coordinator_id = request.query_params.get("id", None)
    coordinators = Coordinator.objects.all()
    if coordinator_id is not None:
        coordinators = coordinators.filter(id=coordinator_id)
    serializer = CoordinatorSerializer(coordinators, many=True)
    return Response(serializer.data)
