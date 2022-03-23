from functools import wraps
from graphql import GraphQLError


def context(f):
    def _context(func):
        def wrapper(*args, **kwargs):
            info = args[f.__code__.co_varnames.index("info")]
            return func(info.context, *args, **kwargs)

        return wrapper

    return _context


def allowed_groups(groups=[]):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            user = context.user
            group = None
            if user.groups.exists():
                group = [g.name for g in user.groups.all()]
                if set(group).intersection(set(groups)):
                    return f(*args, **kwargs)
            raise GraphQLError("You do not have permission to perform this action")

        return wrapper

    return decorator
