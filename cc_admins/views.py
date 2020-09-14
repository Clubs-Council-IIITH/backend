from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.shortcuts import render

from .serializers import LogSerializer, ClubSerializer, CoordinatorSerializer
from organizers.serializers import UpdateSerializer

from base.models import Club, Coordinator, Event
from base.decorators import allowed_groups
from auditlog.models import LogEntry
from organizers.models import Update

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


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


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def updates_new(request):
    serializer = UpdateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def updates_edit(request, id):
    update = Update.objects.get(id=id)
    serializer = UpdateSerializer(instance=update, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["cc_admin"])
def updates_delete(request, id):
    update = Update.objects.get(id=id)
    update.delete()
    return Response("Deleted Successfully")
