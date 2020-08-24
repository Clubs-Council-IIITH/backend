from django.shortcuts import render
from django.utils import timezone

from .serializers import EventSerializer, BudgetProposalSerializer
from .models import BudgetProposal

from base.decorators import allowed_groups
from base.models import Event, Club

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


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
        serializer.save()
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
    return Response("Deleted Successfully")


@permission_classes([IsAuthenticated])
@api_view(["GET"])
@parser_classes([MultiPartParser, FormParser])
@allowed_groups(allowed_roles=["organizer", "cc_admin"])
def proposals(request):
    club = request.query_params.get("club", None)
    token = request.headers.get("Authorization", None)
    proposals = BudgetProposal.objects.all().order_by("-datetime")

    # Filter by club
    if club is not None:
        proposals = proposals.filter(club=club)
    if token:
        mail = Token.objects.get(key=token[6:]).user
        club = Club.objects.filter(mail=mail).first()
        if club:
            proposals = proposals.filter(club=club)

    serializer = BudgetProposalSerializer(proposals, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@allowed_groups(allowed_roles=["organizer"])
def proposals_new(request):
    serializer = BudgetProposalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data["club"] = Club.objects.filter(mail=request.user.username).first()
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

