import graphene
import authentication.schema
import club_manager.schema
import event_manager.schema
import user_manager.schema
import finance_manager.schema
import misc.schema


class Query(
    authentication.schema.Query,
    club_manager.schema.Query,
    event_manager.schema.Query,
    user_manager.schema.Query,
    finance_manager.schema.Query,
    misc.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    authentication.schema.Mutation,
    club_manager.schema.Mutation,
    event_manager.schema.Mutation,
    user_manager.schema.Mutation,
    finance_manager.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
