import graphene
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import superuser_required
from authentication.decorators import allowed_groups

from django.db import IntegrityError
from django.contrib.auth.models import User as AuthUser, Group

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

    instagram = graphene.String()
    facebook = graphene.String()
    youtube = graphene.String()
    twitter = graphene.String()
    linkedin = graphene.String()
    discord = graphene.String()

    img = Upload(required=False)


class AdminCreateClub(graphene.Mutation):
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

        if club_data.instagram:
            club_instance.instagram = club_data.instagram
        if club_data.facebook:
            club_instance.facebook = club_data.facebook
        if club_data.youtube:
            club_instance.youtube = club_data.youtube
        if club_data.twitter:
            club_instance.twitter = club_data.twitter
        if club_data.linkedin:
            club_instance.linkedin = club_data.linkedin
        if club_data.discord:
            club_instance.discord = club_data.discord

        club_instance.save()

        try:
            user = AuthUser.objects.create_user(
                club_data.mail, email=club_data.mail, first_name=club_data.name)
        except IntegrityError:
            user = AuthUser.objects.get(username=club_data.mail)
        Group.objects.get(name="club").user_set.add(user)

        return AdminCreateClub(club=club_instance)


class AdminUpdateClub(graphene.Mutation):
    class Arguments:
        club_data = ClubInput(required=True)

    club = graphene.Field(ClubType)

    @classmethod
    @superuser_required
    def mutate(cls, root, info, club_data=None):
        club_instance = Club.objects.get(pk=club_data.id)

        if club_instance:
            # get the corresponding club user
            user_instance = AuthUser.objects.get(username=club_instance.mail)

            # required fields
            if club_data.img:
                club_instance.img = club_data.img
            if club_data.name:
                club_instance.name = club_data.name
                user_instance.first_name = club_data.name
            if club_data.mail:
                club_instance.mail = club_data.mail
                user_instance.email = club_data.mail
                user_instance.username = club_data.mail

            # optional fields
            club_instance.website = club_data.website
            club_instance.category = club_data.category
            club_instance.tagline = club_data.tagline
            club_instance.description = club_data.description

            club_instance.instagram = club_data.instagram
            club_instance.facebook = club_data.facebook
            club_instance.youtube = club_data.youtube
            club_instance.twitter = club_data.twitter
            club_instance.linkedin = club_data.linkedin
            club_instance.discord = club_data.discord

            club_instance.save()
            user_instance.save()
            return AdminUpdateClub(club=club_instance)

        return AdminUpdateClub(club=None)


class UpdateClub(graphene.Mutation):
    class Arguments:
        club_data = ClubInput(required=True)

    club = graphene.Field(ClubType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, root, info, club_data=None):
        club_instance = Club.objects.get(pk=club_data.id)

        if club_instance:
            if club_data.img:
                club_instance.img = club_data.img
            if club_data.description:
                club_instance.description = club_data.description
            if club_data.name:
                club_instance.name = club_data.name
            if club_data.website:
                club_instance.website = club_data.website
            if club_data.tagline:
                club_instance.tagline = club_data.tagline

            if club_data.instagram:
                club_instance.instagram = club_data.instagram
            if club_data.facebook:
                club_instance.facebook = club_data.facebook
            if club_data.youtube:
                club_instance.youtube = club_data.youtube
            if club_data.twitter:
                club_instance.twitter = club_data.twitter
            if club_data.linkedin:
                club_instance.linkedin = club_data.linkedin
            if club_data.discord:
                club_instance.discord = club_data.discord

            club_instance.save()
            return UpdateClub(club=club_instance)

        return UpdateClub(club=None)


class AdminDeleteClub(graphene.Mutation):
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
            return AdminDeleteClub(club=club_instance)

        return AdminDeleteClub(club=None)
