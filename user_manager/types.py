from graphene_django.types import DjangoObjectType
from user_manager.models import User, Member


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"

    def resolve_img(self, info):
        if self.img:
            return info.context.build_absolute_uri(self.img.url)

        return self.img


class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        fields = "__all__"
