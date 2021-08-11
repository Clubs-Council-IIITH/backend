import graphene
import authentication.schema
import club_manager.schema


class Query(
    authentication.schema.Query,
    club_manager.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    authentication.schema.Mutation,
    club_manager.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
