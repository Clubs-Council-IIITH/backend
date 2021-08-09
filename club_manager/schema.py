import graphene
from club_manager.models import Club
from club_manager.types import ClubType

from club_manager.mutations import CreateClub, DeleteClub, UpdateClub


class Query(graphene.ObjectType):
    clubs = graphene.List(ClubType)
    club = graphene.Field(ClubType, club_id=graphene.Int())

    def resolve_clubs(self, info, **kwargs):
        return Club.objects.all().order_by("name")

    def resolve_club(self, info, club_id):
        return Club.objects.get(pk=club_id)


class Mutation(graphene.ObjectType):
    create_club = CreateClub.Field()
    update_club = UpdateClub.Field()
    delete_club = DeleteClub.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
