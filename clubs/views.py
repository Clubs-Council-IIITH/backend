from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models.functions import Lower
from django.db import IntegrityError
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from common.decorators import allowed_groups

from .models import Club, Event, EventLog, Coordinator
from .serializers import ClubSerializer, EventSerializer, EventLogSerializer, CoordinatorSerializer

from re import split

# EventLog R Endpoint {{{
@permission_classes([IsAuthenticated])
@api_view(["GET"])
@allowed_groups(allowed_roles=["cc_admin"])
def logs(request):
    club = request.query_params.get("club", None)
    logs = EventLog.objects.all()
    if club is not None:
        logs = logs.filter(club=club).order_by("-datetime")
    serializer = EventLogSerializer(logs, many=True)
    return Response(serializer.data)


# }}}

# Events CRUD Endpoints {{{
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


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["organizer"])
def events_new(request):
    context = {"request": request}
    serializer = EventSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.validated_data["club"] = Club.objects.filter(mail=request.user.username).first()
        event = serializer.save()
        log = EventLog.create_event(event)
        log.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["organizer", "cc_admin"])
def events_edit(request, id):
    event = Event.objects.get(id=id)
    if (
        "cc_admin" not in [group.name for group in request.user.groups.all()]
        and event.club != Club.objects.filter(mail=request.user.username).first()
    ):
        return Response("Unauthorized!")
    context = {"request": request}
    serializer = EventSerializer(instance=event, data=request.data, context=context)
    if serializer.is_valid():
        event = serializer.save()
        log = EventLog.update_event(event)
        log.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["organizer", "cc_admin"])
def events_delete(request, id):
    event = Event.objects.get(id=id)
    if (
        "cc_admin" not in [group.name for group in request.user.groups.all()]
        and event.club != Club.objects.filter(mail=request.user.username).first()
    ):
        return Response("Unauthorized!")
    event.state = "deleted"
    event.save()
    log = EventLog.delete_event(event)
    log.save()
    return Response("Deleted Successfully")


# }}}

# Clubs CRUD Endpoints {{{
@api_view(["GET"])
def clubs(request):
    club_id = request.query_params.get("id", None)
    clubs = Club.objects.all().order_by(Lower("name"))
    if club_id is not None:
        clubs = clubs.filter(id=club_id)
    serializer = ClubSerializer(clubs, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def clubs_new(request):
    context = {"request": request}
    serializer = ClubSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        try:
            user = User.objects.create_user(str(serializer.data["mail"]))
        except IntegrityError:
            user = User.objects.get(username=str(serializer.data["mail"]))
        Group.objects.get(name="organizer").user_set.add(user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["GET", "POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def clubs_edit(request, id):
    club = Club.objects.get(id=id)
    Group.objects.get(name="organizer").user_set.remove(User.objects.get(username=club.mail))
    context = {"request": request}
    serializer = ClubSerializer(instance=club, data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        try:
            user = User.objects.create_user(str(serializer.data["mail"]))
        except IntegrityError:
            user = User.objects.get(username=str(serializer.data["mail"]))
        Group.objects.get(name="organizer").user_set.add(user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def clubs_delete(request, id):
    club = Club.objects.get(id=id)
    Group.objects.get(name="organizer").user_set.remove(User.objects.get(username=club.mail))
    club.state = "deleted"
    club.save()
    return Response("Deleted Successfully")


# }}}

# Coordinators CRUD Endpoints {{{
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


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def coordinators_new(request):
    context = {"request": request}
    serializer = CoordinatorSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["GET", "POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def coordinators_edit(request, id):
    coordinator = Coordinator.objects.get(id=id)
    if request.method == "POST":
        context = {"request": request}
        serializer = CoordinatorSerializer(instance=coordinator, data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = ClubSerializer(coordinator)
        return Response(serializer.data)


# }}}
