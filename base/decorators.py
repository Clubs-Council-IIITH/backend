from django.shortcuts import redirect

from rest_framework.response import Response


def allowed_groups(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = [g.name for g in request.user.groups.all()]
                if set(group).intersection(set(allowed_roles)):
                    return view_func(request, *args, **kwargs)
            return Response("Unauthorized!")

        return wrapper

    return decorator
