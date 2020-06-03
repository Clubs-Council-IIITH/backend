from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required


@login_required
def get_token(request):
    user = request.user
    usergroup = "enduser"
    if user.groups.exists():
        usergroup = user.groups.all()[0].name
    token, created = Token.objects.get_or_create(user=user)
    context = {"token": token.key, "usergroup": usergroup}
    return render(request, "login_redirect.html", context)
