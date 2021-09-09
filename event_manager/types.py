from graphene_django.types import DjangoObjectType
from event_manager.models import Event


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"
