from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required


@login_required
def get_token(request):
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    return JsonResponse({"token": token.key})
