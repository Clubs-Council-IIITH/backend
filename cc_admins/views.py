from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.models import User, Group

from auditlog.models import LogEntry
from base.decorators import allowed_groups
from base.models import Club, Coordinator, Event

from .serializers import LogSerializer, ClubSerializer, CoordinatorSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


# Auditlog R
@permission_classes([IsAuthenticated])
@api_view(["GET"])
@allowed_groups(allowed_roles=["cc_admin"])
def logs(request):
    events = request.query_params.get("events", None)
    logs = LogEntry.objects.all()
    if events is not None:
        logs = logs.filter(object_pk__in=events.split(","))
    serializer = LogSerializer(logs, many=True)
    return Response(serializer.data)


# Clubs CUD
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
    return Response(serializer.errors)


@permission_classes([IsAuthenticated])
@api_view(["GET", "POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def clubs_edit(request, id):
    club = Club.objects.get(id=id)
    context = {"request": request}
    serializer = ClubSerializer(instance=club, data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def clubs_delete(request, id):
    club = Club.objects.get(id=id)
    club.state = "deleted"
    club.save()
    return Response("Deleted Successfully")


# Coordinator CUD
@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def coordinators_new(request):
    context = {"request": request}
    serializer = CoordinatorSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


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
        return Response(serializer.errors)
    else:
        serializer = ClubSerializer(coordinator)
        return Response(serializer.data)
