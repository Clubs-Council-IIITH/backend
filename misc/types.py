from graphene_django.types import DjangoObjectType
from misc.models import COC


class COCType(DjangoObjectType):
    class Meta:
        model = COC
        fields = "__all__"
