import graphene
from graphene_file_upload.scalars import Upload

from club_manager.models import Club
from club_manager.types import ClubType


# TODO: implement file uploads
class ClubInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    mail = graphene.String()
    website = graphene.String()
    category = graphene.String()
    state = graphene.String()
    img = Upload(required=False)


class CreateClub(graphene.Mutation):
    class Arguments:
        club_data = ClubInput(required=True)

    club = graphene.Field(ClubType)

    @classmethod
    def mutate(cls, root, info, club_data=None):
        club_instance = Club(
            name=club_data.name,
            mail=club_data.mail,
            website=club_data.website,
            category=club_data.category,
            state=club_data.state,
        )
        club_instance.save()
        return CreateClub(club=club_instance)


class UpdateClub(graphene.Mutation):
    class Arguments:
        club_data = ClubInput(required=True)

    club = graphene.Field(ClubType)

    @classmethod
    def mutate(cls, root, info, club_data=None):
        club_instance = Club.objects.get(pk=club_data.id)

        if club_instance:
            club_instance.name = club_data.name
            club_instance.mail = club_data.mail
            club_instance.website = club_data.website
            club_instance.category = club_data.category
            club_instance.state = club_data.state
            club_instance.save()
            return UpdateClub(club=club_instance)

        return UpdateClub(club=None)


class DeleteClub(graphene.Mutation):
    class Arguments:
        club_data = ClubInput(required=True)

    club = graphene.Field(ClubType)

    @classmethod
    def mutate(cls, root, info, club_data=None):
        club_instance = Club.objects.get(pk=club_data.id)

        if club_instance:
            club_instance.state = "deleted"
            club_instance.save()
            return DeleteClub(club=club_instance)

        return DeleteClub(club=None)
