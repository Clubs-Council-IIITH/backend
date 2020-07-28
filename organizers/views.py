from django.shortcuts import render
from .serializers import EventSerializer
from base.models import Event, Club
from base.decorators import allowed_groups
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


# Events CUD
@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["organizer"])
def events_new(request):
    context = {"request": request}
    serializer = EventSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.validated_data["club"] = Club.objects.filter(mail=request.user.username).first()
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


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
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["organizer", "cc_admin"])
def events_delete(request, id):
    event = Event.objects.get(id=id)
    if event.club != Club.objects.filter(mail=request.user.username).first():
        return Response("Unauthorized!")
    event.state = "deleted"
    event.save()
    return Response("Deleted Successfully")

