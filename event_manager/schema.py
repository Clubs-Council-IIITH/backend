import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import superuser_required
from event_manager.models import Event
from event_manager.types import EventType
from club_manager.models import Club


class Query(graphene.ObjectType):
    # public queries
    all_events = graphene.List(EventType)
    club_events = graphene.List(EventType, club_id=graphene.Int())
    event = graphene.Field(EventType, event_id=graphene.Int())

    def resolve_all_events(self, info, **kwargs):
        return Event.objects.filter(state__in=["published", "completed"]).order_by("start")

    def resolve_club_events(self, info, club_id):
        user = info.context.user
        club = Club.objects.get(pk=club_id)

        # don't show deleted club events to the public
        if club.state != "active" and not user.is_superuser:
            raise GraphQLError("You do not have permission to access this resource.")

        return Event.objects.filter(
            club__pk=club_id, state__in=["published", "completed"]
        ).order_by("start")

    def resolve_event(self, info, event_id):
        user = info.context.user
        event = Event.objects.get(pk=event_id)
        club = Club.objects.get(pk=event.club.pk)

        # don't show deleted club event to the public
        if club.state != "active" and not user.is_superuser:
            raise GraphQLError("You do not have permission to access this resource.")

        return event

    # admin queries
    admin_all_events = graphene.List(EventType)
    admin_club_events = graphene.List(EventType, club_id=graphene.Int())

    @superuser_required
    def resolve_admin_all_events(self, info, **kwargs):
        return Event.objects.order_by("start")

    def resolve_admin_club_events(self, info, club_id):
        return Event.objects.filter(club__pk=club_id).order_by("start")


schema = graphene.Schema(query=Query)
