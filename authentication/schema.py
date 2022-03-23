import graphene
import graphql_jwt
from graphene.types.generic import GenericScalar
from graphql_jwt.utils import get_payload
from graphql_jwt.decorators import ensure_token


class Query(graphene.ObjectType):
    payload = GenericScalar(required=True)

    @classmethod
    @ensure_token
    def resolve_payload(cls, root, info, token, **kwargs):
        return get_payload(token, info.context)


class Mutation(graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token = graphql_jwt.DeleteJSONWebTokenCookie.Field()


schema = graphene.Schema(mutation=Mutation)
