import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import superuser_required

from misc.models import COC
from misc.types import COCType


class Query(graphene.ObjectType):
    scoreboard = graphene.List(COCType)

    def resolve_scoreboard(self, info, **kwargs):
        return COC.objects.all().order_by("-score")


schema = graphene.Schema(query=Query)
