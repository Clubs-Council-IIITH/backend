import graphene
from graphene_file_upload.scalars import Upload

from event_manager.models import Event
from event_manager.types import EventType

from club_manager.models import Club


class EventInput(graphene.InputObjectType):
    id = graphene.ID()
    poster = Upload(required=False)
    start = graphene.DateTime()
    end = graphene.DateTime()
    name = graphene.String()
    description = graphene.String()
    venue = graphene.String()
    audience = graphene.String()
    last_edited_by = graphene.String()


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
            start=event_data.start,
            end=event_data.end,
            description=event_data.description,
            venue=event_data.venue,
            audience=event_data.audience,
            last_edited_by=event_data.last_edited_by,
        )

        # optional fields
        if event_data.poster:
            event_instance.poster = event_data.poster

        event_instance.save()

        return CreateEvent(event=event_instance)
