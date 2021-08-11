import graphene
import club_manager.schema


class Query(
    club_manager.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    club_manager.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
