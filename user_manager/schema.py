import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import superuser_required

from user_manager.models import User, Member
from user_manager.types import UserType, MemberType
from user_manager.mutations import (
    CreateUser,
    UpdateUser,
    AddMember,
    UpdateMember,
    RemoveMember,
)

from club_manager.models import Club


class Query(graphene.ObjectType):
    # public queries
    club_members = graphene.List(MemberType, club_id=graphene.Int())
    user = graphene.Field(UserType, mail=graphene.String())

    def resolve_club_members(self, info, club_id):
        return Member.objects.filter(club__pk=club_id, approved=True)

    def resolve_user(self, info, mail):
        return User.objects.get(mail=mail)

    # admin queries
    admin_club_members = graphene.List(MemberType)

    def resolve_admin_club_members(self, info):
        club = Club.objects.get(mail=info.context.user.username)
        return Member.objects.filter(club__pk=club.id)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    add_member = AddMember.Field()
    update_member = UpdateMember.Field()
    remove_member = RemoveMember.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
