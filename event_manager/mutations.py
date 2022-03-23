import graphene
from graphene_file_upload.scalars import Upload

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
    venue = graphene.String()
    audience = graphene.String()
    lastEditedBy = graphene.String()
    financialRequirements = graphene.String()


class CreateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    # TODO: protect mutation
    def mutate(cls, root, info, event_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)

        event_instance = Event(
            club=club,
            name=event_data.name,
            datetimeStart=event_data.datetimeStart,
            datetimeEnd=event_data.datetimeEnd,
            lastEditedBy=event_data.lastEditedBy,
        )

        # optional fields
        if event_data.poster:
            event_instance.poster = event_data.poster
        if event_data.audience:
            event_instance.audience = event_data.audience
        if event_data.description:
            event_instance.description = event_data.description
        if event_data.venue:
            event_instance.venue = event_data.venue
        if event_data.financialRequirements:
            event_instance.financialRequirements = event_data.financialRequirements

        event_instance.save()

        return CreateEvent(event=event_instance)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    # TODO: protect mutation
    def mutate(cls, root, info, event_data=None):
        event_instance = Event.objects.get(pk=event_data.id)

        if event_instance:
            # required fields
            if event_data.name:
                event_instance.name = event_data.name
            if event_data.datetimeStart:
                event_instance.datetimeStart = event_data.datetimeStart
            if event_data.datetimeEnd:
                event_instance.datetimeEnd = event_data.datetimeEnd
            if event_data.lastEditedBy:
                event_instance.lastEditedBy = event_data.lastEditedBy

            # optional fields
            event_instance.poster = event_data.poster
            event_instance.audience = event_data.audience
            event_instance.description = event_data.description
            event_instance.venue = event_data.venue
            event_instance.financialRequirements = event_data.financialRequirements

            event_instance.save()
            return UpdateEvent(event=event_instance)

        return UpdateEvent(event=None)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    # TODO: protect mutation
    def mutate(cls, root, info, event_data=None):
        event_instance = Event.objects.get(pk=event_data.id)

        if event_instance:
            event_instance.state = "deleted"
            event_instance.save()
            return DeleteEvent(event=event_instance)

        return DeleteEvent(event=event_instance)
