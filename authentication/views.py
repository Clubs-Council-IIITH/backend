from datetime import datetime
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.utils import jwt_payload, jwt_encode
from graphql_jwt.settings import jwt_settings
from club_manager.models import Club

groups = {
    "club": "club",
    "clubs_council": "clubs_council",
    "finance_council": "finance_council",
    "slo": "slo",
    "slc": "slc",
}


@csrf_exempt
@login_required(login_url="/accounts/login")
def jwt(request, **kwargs):
    user_groups = list(request.user.groups.values_list("name", flat=True))

    # populate payload
    payload = jwt_payload(request.user)
    payload["id"] = request.user.id
    payload["group"] = user_groups[0] if len(user_groups) else None
    payload["isAuthenticated"] = True
    payload["props"] = dict()

    # populate group specific properties
    if payload["group"] == groups["club"]:
        payload["props"]["club"] = {"id": Club.objects.get(mail=request.user.username).id}

    # generate token
    token = jwt_encode(payload)

    # cookie config
    expires = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA
    kwargs = {
        "expires": expires,
        "httponly": True,
        "secure": jwt_settings.JWT_COOKIE_SECURE,
        "path": jwt_settings.JWT_COOKIE_PATH,
        "domain": jwt_settings.JWT_COOKIE_DOMAIN,
        "samesite": jwt_settings.JWT_COOKIE_SAMESITE,
    }

    response = HttpResponseRedirect(settings.CAS_CLIENT_URL)
    response.set_cookie(jwt_settings.JWT_COOKIE_NAME, token, **kwargs)

    return response
