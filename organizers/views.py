from django.shortcuts import render
from .serializers import EventSerializer
from base.models import Event
from base.decorators import allowed_groups

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


@permission_classes([IsAuthenticated])
@api_view(["GET"])
@allowed_groups(allowed_roles=["organizer", "cc_admin"])
def events_filter(request):
    token = request.headers.get("Authorization")[6:]
    club = Token.objects.get(key=token).user
    events = Event.objects.filter(club=club)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["organizer"])
def events_new(request):
    context = {"request": request}
    serializer = EventSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@allowed_groups(allowed_roles=["organizer"])
def events_delete(request, id):
    event = Event.objects.get(id=id)
    if request.user.username != event.user:
        return Response("Unauthorized!")
    event.state = "deleted"
    event.save()
    return Response("Deleted Successfully")


@permission_classes([IsAuthenticated])
@api_view(["GET", "POST"])
@allowed_groups(allowed_roles=["organizer", "cc_admin"])
def events_edit(request, id):
    event = Event.objects.get(id=id)
    if (
        "cc_admin" not in [group.name for group in request.user.groups.all()]
        and request.user.username != event.user
    ):
        return Response("Unauthorized!")
    if request.method == "POST":
        context = {"request": request}
        serializer = EventSerializer(instance=event, data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    else:
        serializer = EventSerializer(event)
        return Response(serializer.data)
