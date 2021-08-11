from datetime import datetime
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.utils import jwt_payload, jwt_encode
from graphql_jwt.settings import jwt_settings


@csrf_exempt
@login_required(login_url="/accounts/login")
def jwt(request, **kwargs):
    payload = jwt_payload(request.user)
    token = jwt_encode(payload)
    expires = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA

    kwargs = {
        "expires": expires,
        "httponly": True,
        "secure": jwt_settings.JWT_COOKIE_SECURE,
        "path": jwt_settings.JWT_COOKIE_PATH,
        "domain": jwt_settings.JWT_COOKIE_DOMAIN,
        "samesite": jwt_settings.JWT_COOKIE_SAMESITE,
    }

    print(f"jwt: {token}")

    response = HttpResponseRedirect(settings.CAS_CLIENT_URL)
    response.set_cookie(jwt_settings.JWT_COOKIE_NAME, token, **kwargs)

    return response
