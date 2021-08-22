import graphene
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import superuser_required

from club_manager.models import Club
from club_manager.types import ClubType


class ClubInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    mail = graphene.String()
    website = graphene.String()
    category = graphene.String()
    state = graphene.String()
    tagline = graphene.String()
    description = graphene.String()
    img = Upload(required=False)


class CreateClub(graphene.Mutation):
    class Arguments:
        club_data = ClubInput(required=True)

    club = graphene.Field(ClubType)

    @classmethod
    @superuser_required
    def mutate(cls, root, info, club_data=None):
        club_instance = Club(
            name=club_data.name,
            mail=club_data.mail,
            category=club_data.category,
        )

        # optional fields
        if club_data.img:
            club_instance.img = club_data.img
        if club_data.website:
            club_instance.website = club_data.website
        if club_data.tagline:
            club_instance.tagline = club_data.tagline
        if club_data.description:
            club_instance.description = club_data.description

        club_instance.save()
        return CreateClub(club=club_instance)


class UpdateClub(graphene.Mutation):
    class Arguments:
        club_data = ClubInput(required=True)

    club = graphene.Field(ClubType)

    @classmethod
    @superuser_required
    def mutate(cls, root, info, club_data=None):
        club_instance = Club.objects.get(pk=club_data.id)

        if club_instance:
            # required fields
            if club_data.img:
                club_instance.img = club_data.img
            if club_data.name:
                club_instance.name = club_data.name
            if club_data.mail:
                club_instance.mail = club_data.mail

            club_instance.website = club_data.website
            club_instance.category = club_data.category
            club_instance.tagline = club_data.tagline
            club_instance.description = club_data.description
            club_instance.save()
            return UpdateClub(club=club_instance)

        return UpdateClub(club=None)


class DeleteClub(graphene.Mutation):
    class Arguments:
        club_data = ClubInput(required=True)

    club = graphene.Field(ClubType)

    @classmethod
    @superuser_required
    def mutate(cls, root, info, club_data=None):
        club_instance = Club.objects.get(pk=club_data.id)

        if club_instance:
            club_instance.state = "deleted"
            club_instance.save()
            return DeleteClub(club=club_instance)

        return DeleteClub(club=None)
