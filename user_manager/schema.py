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


class Query(graphene.ObjectType):
    # public queries
    club_members = graphene.List(MemberType, club_id=graphene.Int())
    user = graphene.Field(UserType, mail=graphene.String())

    def resolve_club_members(self, info, club_id):
        return Member.objects.filter(club__pk=club_id)

    def resolve_user(self, info, mail):
        return User.objects.get(mail=mail)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    add_member = AddMember.Field()
    update_member = UpdateMember.Field()
    remove_member = RemoveMember.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
