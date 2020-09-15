from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from common.decorators import allowed_groups

from clubs.models import Club
from .models import Proposal
from .serializers import ProposalSerializer


# Budget Proposals CR Endpoints {{{
@permission_classes([IsAuthenticated])
@api_view(["GET"])
@parser_classes([MultiPartParser, FormParser])
@allowed_groups(allowed_roles=["organizer", "cc_admin"])
def proposals(request):
    club = request.query_params.get("club", None)
    token = request.headers.get("Authorization", None)
    proposals = Proposal.objects.all().order_by("-datetime")

    # Filter by club
    if club is not None:
        proposals = proposals.filter(club=club)
    if token:
        mail = Token.objects.get(key=token[6:]).user
        club = Club.objects.filter(mail=mail).first()
        if club:
            proposals = proposals.filter(club=club)

    serializer = ProposalSerializer(proposals, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@allowed_groups(allowed_roles=["organizer"])
def proposals_new(request):
    serializer = ProposalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data["club"] = Club.objects.filter(mail=request.user.username).first()
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# }}}
