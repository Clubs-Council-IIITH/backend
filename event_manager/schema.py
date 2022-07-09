import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import superuser_required

from club_manager.models import Club

from event_manager.models import Event, EVENT_STATE_LIST
from event_manager.types import EventType
from event_manager.mutations import CreateEvent, UpdateEvent, DeleteEvent


EVENT_STATE_DICT = {state[1]: state[0] for state in EVENT_STATE_LIST}


class Query(graphene.ObjectType):
    # public queries
    all_events = graphene.List(EventType)
    club_events = graphene.List(EventType, club_id=graphene.Int())
    event = graphene.Field(EventType, event_id=graphene.Int())

    def resolve_all_events(self, info, **kwargs):
        # show only approved and completed events to the public
        return Event.objects.filter(
            state__in=[EVENT_STATE_DICT["approved"], EVENT_STATE_DICT["completed"]]
        ).order_by("datetimeStart")

    def resolve_club_events(self, info, club_id):
        user = info.context.user
        club = Club.objects.get(pk=club_id)

        # don't show deleted club events to the public
        if club.state != "active" and not user.is_superuser:
            raise GraphQLError("You do not have permission to access this resource.")

        # show only approved and completed events to the public
        return Event.objects.filter(
            club__pk=club_id,
            state__in=[EVENT_STATE_DICT["approved"], EVENT_STATE_DICT["completed"]],
        ).order_by("datetimeStart")

    def resolve_event(self, info, event_id):
        user = info.context.user
        event = Event.objects.get(pk=event_id)
        club = Club.objects.get(pk=event.club.pk)

        # don't show deleted club's event to the public
        if club.state != "active" and not user.is_superuser:
            raise GraphQLError("You do not have permission to access this resource.")

        return event

    # admin queries
    admin_all_events = graphene.List(EventType)
    admin_club_events = graphene.List(EventType, club_id=graphene.Int())

    @superuser_required
    def resolve_admin_all_events(self, info, **kwargs):
        return Event.objects.order_by("datetimeStart")

    def resolve_admin_club_events(self, info, club_id):
        return Event.objects.filter(club__pk=club_id).order_by("datetimeStart")


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
