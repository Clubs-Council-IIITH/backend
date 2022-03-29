import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

from user_manager.models import User, Member
from user_manager.types import UserType, MemberType

from club_manager.models import Club
from authentication.decorators import allowed_groups


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    img = Upload(required=False)
    firstName = graphene.String()
    lastName = graphene.String()
    mail = graphene.String()
    batch = graphene.String()


class MemberInput(graphene.InputObjectType):
    id = graphene.ID()
    userId = graphene.ID()
    role = graphene.String()
    year = graphene.Int()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(UserType)

    @classmethod
    @allowed_groups(["club", "clubs_council"])
    def mutate(cls, root, info, user_data=None):
        user_instance = User(
            firstName=user_data.firstName,
            lastName=user_data.lastName,
            mail=user_data.mail,
            batch=user_data.batch,
        )

        # optional fields
        if user_data.img:
            user_instance.img = user_data.img

        user_instance.save()

        return CreateUser(user=user_instance)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(UserType)

    @classmethod
    @allowed_groups(["club", "clubs_council"])
    def mutate(cls, root, info, user_data=None):
        user_instance = User.objects.get(pk=user_data.id)

        if user_instance:
            # required fields
            if user_data.firstName:
                user_instance.firstName = user_data.firstName
            if user_data.lastName:
                user_instance.lastName = user_data.lastName
            if user_data.mail:
                user_instance.mail = user_data.mail
            if user_data.batch:
                user_instance.batch = user_data.batch
            if user_data.img:
                user_instance.img = user_data.img

            user_instance.save()
            return UpdateUser(user=user_instance)

        return UpdateUser(user=None)


class AddMember(graphene.Mutation):
    class Arguments:
        member_data = MemberInput(required=True)

    member = graphene.Field(MemberType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, root, info, member_data=None):
        user = User.objects.get(pk=member_data.userId)
        club = Club.objects.get(mail=info.context.user.username)

        # check if member is already in the club for the given year
        member = Member.objects.filter(user=user, club=club, year=member_data.year)
        if len(member):
            raise GraphQLError("Member already exists!")

        member_instance = Member(
            user=user,
            club=club,
            role=member_data.role,
            year=member_data.year,
        )
        member_instance.save()

        return AddMember(member=member_instance)


class UpdateMember(graphene.Mutation):
    class Arguments:
        member_data = MemberInput(required=True)

    member = graphene.Field(MemberType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, root, info, member_data=None):
        member_instance = Member.objects.get(pk=member_data.id)

        if member_instance:
            # required fields
            if member_data.role:
                member_instance.role = member_data.role
            if member_data.year:
                member_instance.year = member_data.year

            # queue member for approval again
            member_instance.approved = False

            member_instance.save()
            return UpdateMember(member=member_instance)

        return UpdateMember(member=None)


class RemoveMember(graphene.Mutation):
    class Arguments:
        member_data = MemberInput(required=True)

    member = graphene.Field(MemberType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, root, info, member_data=None):
        member_instance = Member.objects.get(pk=member_data.id)

        if member_instance:
            member_instance.delete()

        return RemoveMember(member=None)


class AdminApproveMember(graphene.Mutation):
    class Arguments:
        member_data = MemberInput(required=True)

    member = graphene.Field(MemberType)

    @classmethod
    @allowed_groups(["clubs_council"])
    def mutate(cls, root, info, member_data=None):
        member_instance = Member.objects.get(pk=member_data.id)

        if member_instance:
            member_instance.approved = True

            member_instance.save()
            return AdminApproveMember(member=member_instance)
        return AdminApproveMember(member=None)
