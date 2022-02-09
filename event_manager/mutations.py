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
    def mutate(cls, root, info, event_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)

        event_instance = Event(
            club=club,
            name=event_data.name,
            datetimeStart=event_data.datetimeStart,
            datetimeEnd=event_data.datetimeEnd,
            description=event_data.description,
            venue=event_data.venue,
            audience=event_data.audience,
            lastEditedBy=event_data.lastEditedBy,
            financialRequirements=event_data.financialRequirements,
        )

        # optional fields
        if event_data.poster:
            event_instance.poster = event_data.poster

        event_instance.save()

        return CreateEvent(event=event_instance)
