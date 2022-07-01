import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

from authentication.decorators import allowed_groups

from event_manager.models import Event
from event_manager.types import EventType

from club_manager.models import Club


class EventInput(graphene.InputObjectType):
    id = graphene.ID()
    poster = Upload(required=False)
    datetimeStart = graphene.DateTime()
    datetimeEnd = graphene.DateTime()
    name = graphene.String()
    description = graphene.String()
    audience = graphene.String()
    mode = graphene.String()


class CreateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club", "clubs_council"])
    def mutate(cls, root, info, event_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)

        event_instance = Event(
            club=club,
            name=event_data.name,
            datetimeStart=event_data.datetimeStart,
            datetimeEnd=event_data.datetimeEnd,
            mode=event_data.mode,
        )

        # optional fields
        if event_data.poster:
            event_instance.poster = event_data.poster
        if event_data.audience:
            event_instance.audience = event_data.audience
        if event_data.description:
            event_instance.description = event_data.description

        event_instance.save()

        return CreateEvent(event=event_instance)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, root, info, event_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=event_data.id)

        if event_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError("You do not have permission to access this resource.")

            # required fields
            if event_data.name:
                event_instance.name = event_data.name
            if event_data.datetimeStart:
                event_instance.datetimeStart = event_data.datetimeStart
            if event_data.datetimeEnd:
                event_instance.datetimeEnd = event_data.datetimeEnd
            if event_data.mode:
                event_instance.mode = event_data.mode

            # optional fields
            event_instance.poster = event_data.poster
            event_instance.audience = event_data.audience
            event_instance.description = event_data.description

            event_instance.save()
            return UpdateEvent(event=event_instance)

        return UpdateEvent(event=None)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, root, info, event_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=event_data.id)

        if event_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError("You do not have permission to access this resource.")

            event_instance.state = "deleted"
            event_instance.save()
            return DeleteEvent(event=event_instance)

        return DeleteEvent(event=event_instance)
