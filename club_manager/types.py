from graphene_django.types import DjangoObjectType
from club_manager.models import Club


class ClubType(DjangoObjectType):
    class Meta:
        model = Club
        fields = "__all__"
