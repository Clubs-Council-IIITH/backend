import graphene
from graphene_django.types import DjangoObjectType
from event_manager.models import Event, EventFeedback
from django.contrib.auth.models import User as AuthUser


class AuthUserType(DjangoObjectType):
    class Meta:
        model = AuthUser
        fields = "__all__"


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"

    def resolve_poster(self, info):
        if self.poster:
            return info.context.build_absolute_uri(self.poster.url)

        return self.poster


class EventFeedbackType(DjangoObjectType):
    class Meta:
        model = EventFeedback
        fields = "__all__"


class AvailableRoomType(graphene.ObjectType):
    room = graphene.String()
    available = graphene.Boolean()


class RoomType(graphene.ObjectType):
    room = graphene.String()
    population = graphene.Int()
    equipment = graphene.String()
    additional = graphene.String()
