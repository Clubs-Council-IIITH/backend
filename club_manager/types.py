from django.conf import settings
from graphene_django.types import DjangoObjectType
from club_manager.models import Club


class ClubType(DjangoObjectType):
    class Meta:
        model = Club
        fields = "__all__"

    def resolve_img(self, info):
        return f"http://localhost{settings.MEDIA_URL}{self.img}"
