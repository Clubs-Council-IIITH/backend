import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import superuser_required
from authentication.decorators import allowed_groups

from club_manager.models import Club

from event_manager.models import Event, EVENT_STATE_DICT, EventFeedback
from event_manager.types import EventFeedbackType, EventType
from event_manager.mutations import (
    CreateEvent,
    UpdateEvent,
    DeleteEvent,
    ProgressEvent,
    AddEventFeedback,
)


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
    admin_cc_pending_events = graphene.List(EventType)
    admin_fc_pending_events = graphene.List(EventType)
    admin_gad_pending_events = graphene.List(EventType)
    admin_slo_pending_events = graphene.List(EventType)
    admin_slc_pending_events = graphene.List(EventType)

    event_feedback_thread = graphene.List(EventFeedbackType, event_id=graphene.Int())

    @superuser_required
    def resolve_admin_all_events(self, info, **kwargs):
        return Event.objects.order_by("datetimeStart")

    def resolve_admin_club_events(self, info, club_id):
        return Event.objects.filter(club__pk=club_id).order_by("datetimeStart")

    @allowed_groups(["club", "clubs_council", "finance_council", "slo", "slc", "gad"])
    def resolve_event_feedback_thread(self, info, event_id):
        event = Event.objects.get(pk=event_id)
        feedback_thread = EventFeedback.objects.filter(event=event).order_by("timestamp")

        return feedback_thread

    @allowed_groups(["clubs_council"])
    def resolve_admin_cc_pending_events(self, info, **kwargs):
        events = Event.objects.filter(state=EVENT_STATE_DICT["cc_pending"]).order_by(
            "datetimeStart"
        )

        return events

    @allowed_groups(["finance_council"])
    def resolve_admin_fc_pending_events(self, info, **kwargs):
        events = Event.objects.filter(state=EVENT_STATE_DICT["fc_pending"]).order_by(
            "datetimeStart"
        )

        return events

    @allowed_groups(["gad"])
    def resolve_admin_gad_pending_events(self, info, **kwargs):
        events = Event.objects.filter(state=EVENT_STATE_DICT["gad_pending"]).order_by(
            "datetimeStart"
        )

        return events

    @allowed_groups(["slo"])
    def resolve_admin_slo_pending_events(self, info, **kwargs):
        events = Event.objects.filter(state=EVENT_STATE_DICT["slo_pending"]).order_by(
            "datetimeStart"
        )

        return events

    @allowed_groups(["slc"])
    def resolve_admin_slc_pending_events(self, info, **kwargs):
        events = Event.objects.filter(state=EVENT_STATE_DICT["slc_pending"]).order_by(
            "datetimeStart"
        )

        return events


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()

    progress_event = ProgressEvent.Field()

    add_event_feedback = AddEventFeedback.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
