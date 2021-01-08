from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from .decorators import allowed_groups

from .models import Update
from .serializers import UpdateSerializer

# Authentication Endpoints {{{
@login_required
def get_token(request):
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    context = {"token": token.key, "redirect_url": settings.CAS_REDIRECT_URL}
    return render(request, "login_redirect.html", context)


@api_view(["GET"])
def get_session(request):
    session = {"is_authenticated": False, "user": { "name": None, "group": None } }
    if not request.user.is_anonymous:
        try:
            user = request.user
            session["user"]["name"] = str(user.username)
            session["user"]["group"] = str(user.groups.all()[0])
        except:
            pass
        session["is_authenticated"] = True
    return JsonResponse(session)


@api_view(["GET"])
def end_session(request):
    response = JsonResponse({"logout_url": settings.CAS_LOGOUT_URL})
    response.delete_cookie("sessionid")
    return response


# }}}

# Updates CRUD Endpoints {{{
@permission_classes([IsAuthenticated])
@api_view(["GET"])
@allowed_groups(allowed_roles=["organizer", "cc_admin"])
def updates(request):
    update_id = request.query_params.get("id", None)
    updates = Update.objects.all().order_by("-datetime")
    if update_id is not None:
        updates = updates.filter(id=update_id)
    serializer = UpdateSerializer(updates, many=True)
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


# }}}
