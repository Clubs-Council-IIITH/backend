from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Club, Event, Coordinator

from cc_admins.serializers import ClubSerializer, CoordinatorSerializer
from organizers.serializers import EventSerializer

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from re import split

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
    club = request.query_params.get("club", None)
    token = request.headers.get("Authorization", None)
    events = Event.objects.all().order_by("datetime")

    # Mark past events as Completed
    for event in events:
        if event.datetime < timezone.now() and event.state != "deleted":
            event.state = "completed"
            event.save()

    # Filter by club
    if club is not None:
        events = events.filter(club=club)
    if token:
        mail = Token.objects.get(key=token[6:]).user
        club = Club.objects.filter(mail=mail).first()
        if club:
            events = events.filter(club=club)

    # Filter by event ID
    if event_id is not None:
        events = events.filter(id=event_id)

    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


# Clubs R
@api_view(["GET"])
def clubs(request):
    club_id = request.query_params.get("id", None)
    clubs = Club.objects.all().order_by(Lower("name"))
    if club_id is not None:
        clubs = clubs.filter(id=club_id)
    serializer = ClubSerializer(clubs, many=True)
    return Response(serializer.data)


# Coordinators R
@api_view(["GET"])
def coordinators(request):
    coordinator_id = request.query_params.get("id", None)
    club = request.query_params.get("club", None)
    coordinators = Coordinator.objects.all().order_by(Lower("name"))
    if club is not None:
        coordinators = [obj for obj in coordinators if club in split("\$|\,", obj.roles or "")]
    if coordinator_id is not None:
        coordinators = coordinators.filter(id=coordinator_id)
    serializer = CoordinatorSerializer(coordinators, many=True)
    return Response(serializer.data)
