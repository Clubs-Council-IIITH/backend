from django.shortcuts import render
from .serializers import LogSerializer
from auditlog.models import LogEntry
from base.decorators import allowed_groups

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


@permission_classes([IsAuthenticated])
@api_view(["GET"])
@allowed_groups(allowed_roles=["cc_admins"])
def logs(request):
    logs = LogEntry.objects.all()
    serializer = LogSerializer(logs, many=True)
    print(serializer.data)
    return Response(serializer.data)
