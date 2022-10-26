import graphene
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from event_manager.models import Event, EventDiscussion
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


class EventDiscussionType(DjangoObjectType):
    class Meta:
        model = EventDiscussion
        fields = "__all__"


class AvailableRoomType(graphene.ObjectType):
    room = graphene.String()
    available = graphene.Boolean()


class RoomType(graphene.ObjectType):
    room = graphene.String()
    isapproved = graphene.Boolean()
    population = graphene.Int()
    equipment = graphene.String()
    additional = graphene.String()


class EventInput(graphene.InputObjectType):
    id = graphene.ID()
    datetimeStart = graphene.DateTime()
    datetimeEnd = graphene.DateTime()
    name = graphene.String()
    description = graphene.String()
    audience = graphene.String()


class RoomDetailsInput(graphene.InputObjectType):
    event_id = graphene.ID()
    room = graphene.String()
    population = graphene.Int()
    equipment = graphene.String(required=False)
    additional = graphene.String(required=False)


class ChangePosterInput(graphene.InputObjectType):
    event_id = graphene.ID()
    img = Upload(required=False)
    delete_prev = graphene.Boolean()


class EventDiscussionInput(graphene.InputObjectType):
    event_id = graphene.ID()
    message = graphene.String()
