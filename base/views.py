from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required


@login_required
def get_token(request):
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    context = {"token": token.key}
    return render(request, "login_redirect.html", context)
