from django.shortcuts import render
from .serializers import EventSerializer
from base.models import Event

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def events(request):
    token = request.headers.get("Authorization")[6:]
    user = Token.objects.get(key=token).user
    events = Event.objects.filter(user=user)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def events_new(request):
    context = {"request": request}
    serializer = EventSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def events_delete(request, id):
    event = Event.objects.get(id=id)
    event.state = "deleted"
    event.save()
    return Response("Deleted Successfully")


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def events_edit(request, id):
    event = Event.objects.get(id=id)
    context = {"request": request}
    serializer = EventSerializer(instance=event, data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
