import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import superuser_required
from authentication.decorators import allowed_groups

from club_manager.models import Club

from event_manager.models import Event, EVENT_STATE_DICT, ROOM_LIST, ROOM_DICT, EventDiscussion
from event_manager.types import EventDiscussionType, EventType, AvailableRoomType, RoomType, PocType
from event_manager.mutations import (
    AddPocDetails,
    ApproveCC,
    NewEventDescription,
    UpdateEvent,
    UpdateAudience,
    AddRoomDetails,
    ChangePoster,
    DeleteEvent,
    ProgressEvent,
    BypassBudgetApproval,
    SLCReminder,
    SLOReminder,
    SendDiscussionMessage,
)


class Query(graphene.ObjectType):
    # public queries
    all_events = graphene.List(EventType)
    club_events = graphene.List(EventType, club_id=graphene.Int())
    event = graphene.Field(EventType, event_id=graphene.Int())
    room_by_event_id = graphene.Field(RoomType, event_id=graphene.Int())

    def resolve_all_events(self, info, **kwargs):
        # show only approved and completed events to the public
        return Event.objects.filter(
            state__in=[EVENT_STATE_DICT["approved"],
                       EVENT_STATE_DICT["completed"]]
        ).exclude(
            audience__contains="internal"
        ).order_by("datetimeStart")

    def resolve_club_events(self, info, club_id):
        user = info.context.user
        club = Club.objects.get(pk=club_id)

        # don't show deleted club events to the public
        if club.state != "active" and not user.is_superuser:
            raise GraphQLError(
                "You do not have permission to access this resource.")

        # show only approved and completed events to the public
        return Event.objects.filter(
            club__pk=club_id,
            state__in=[EVENT_STATE_DICT["approved"],
                       EVENT_STATE_DICT["completed"]],
        ).exclude(
            audience__contains="internal"
        ).order_by("datetimeStart")

    def resolve_event(self, info, event_id):
        user = info.context.user
        event = Event.objects.get(pk=event_id)
        club = Club.objects.get(pk=event.club.pk)

        # don't show deleted club's event to the public
        if club.state != "active" and not user.is_superuser:
            raise GraphQLError(
                "You do not have permission to access this resource.")

        return event

    def resolve_room_by_event_id(self, info, event_id):
        event = Event.objects.get(pk=event_id)

        return {
            "room": ROOM_LIST[event.room_id][1]
        }

    # admin queries
    admin_all_events = graphene.List(EventType)
    admin_club_events = graphene.List(EventType, club_id=graphene.Int())
    admin_approved_events = graphene.List(EventType)
    admin_incomplete_events = graphene.List(EventType)
    admin_cc_pending_events = graphene.List(EventType)
    admin_fc_pending_events = graphene.List(EventType)
    admin_gad_pending_events = graphene.List(EventType)
    admin_slo_pending_events = graphene.List(EventType)
    admin_slc_pending_events = graphene.List(EventType)
    admin_available_rooms = graphene.List(
        AvailableRoomType, event_id=graphene.Int())
    admin_room_by_event_id = graphene.Field(RoomType, event_id=graphene.Int())
    admin_poc_by_event_id = graphene.Field(PocType, event_id=graphene.Int())

    event_discussion_thread = graphene.List(
        EventDiscussionType, event_id=graphene.Int())

    @superuser_required
    def resolve_admin_all_events(self, info, **kwargs):
        return Event.objects.order_by("datetimeStart")

    def resolve_admin_club_events(self, info, club_id):
        return Event.objects.filter(club__pk=club_id).order_by("datetimeStart")

    @allowed_groups(["club", "clubs_council", "finance_council", "slo", "slc", "gad"])
    def resolve_event_discussion_thread(self, info, event_id):
        event = Event.objects.get(pk=event_id)
        discussion_thread = EventDiscussion.objects.filter(
            event=event).order_by("timestamp")

        return discussion_thread

    @allowed_groups(["clubs_council", "finance_council", "slo", "slc", "gad"])
    def resolve_admin_approved_events(self, info, **kwargs):
        user_roles = info.context.user.groups
        admin_level = -1
        if user_roles.filter(name="clubs_council").exists():
            admin_level = 1
        if user_roles.filter(name="slc").exists():
            # admin_level = 2
            return Event.objects.filter(
                state__gt=1).filter(
                budget_approved=True
            ).order_by("-datetimeStart")
        if user_roles.filter(name="slo").exists():
            # admin_level = 2
            return Event.objects.filter(
                room_approved=True
            ).filter(state__gt=1).order_by("-datetimeStart")
        if user_roles.filter(name="gad").exists():
            admin_level = 2

        # print(admin_level)

        return Event.objects.filter(state__gt=admin_level).order_by("-datetimeStart")

    @allowed_groups(["clubs_council"])
    def resolve_admin_cc_pending_events(self, info, **kwargs):
        events = Event.objects.filter(state=EVENT_STATE_DICT["cc_pending"]).order_by(
            "datetimeStart"
        )

        return events

    @allowed_groups(["clubs_council"])
    def resolve_admin_incomplete_events(self, info, **kwargs):
        events = Event.objects.filter(state=EVENT_STATE_DICT["incomplete"]).order_by(
            "datetimeStart"
        )

        return events

    @allowed_groups(["finance_council"])
    def resolve_admin_fc_pending_events(self, info, **kwargs):
        events = Event.objects.filter(
            state=EVENT_STATE_DICT["room|budget_pending"]
        ).filter(
            budget_approved=False
        ).order_by(
            "datetimeStart"
        )

        return events

    @allowed_groups(["slo"])
    def resolve_admin_slo_pending_events(self, info, **kwargs):
        events = Event.objects.filter(
            state=EVENT_STATE_DICT["room|budget_pending"]
        ).filter(
            room_approved=False
            # ).exclude(
            #     room_id=0
        ).order_by(
            "datetimeStart"
        )

        return events

    @allowed_groups(["slc"])
    def resolve_admin_slc_pending_events(self, info, **kwargs):
        events = Event.objects.filter(
            state=EVENT_STATE_DICT["room|budget_pending"]
        ).filter(
            budget_approved=False
        ).order_by(
            "datetimeStart"
        )

        return events

    @allowed_groups(["gad"])
    def resolve_admin_gad_pending_events(self, info, **kwargs):
        events = Event.objects.filter(
            state=EVENT_STATE_DICT["room|budget_pending"]
        ).filter(
            room_approved=False
        ).exclude(
            room_id=0
        ).order_by(
            "datetimeStart"
        )

        return events

    @allowed_groups(["club", "clubs_council", "finance_council", "slo", "slc", "gad"])
    def resolve_admin_available_rooms(self, info, event_id):
        otherEvents = Event.objects.filter(
            room_approved=True).exclude(pk=event_id)
        # for testing ->
        # otherEvents = Event.objects.exclude(pk=event_id)
        event = Event.objects.get(pk=event_id)
        availablity = {idx: True for idx, _ in ROOM_LIST}
        for otherEvent in otherEvents:
            # check if the other event's room is not none
            if otherEvent.room_id != ROOM_DICT["none"]:
                # check if the room is available and the time slot collides with this event's time slot
                if (
                    availablity[otherEvent.room_id]
                    and event.datetimeEnd > otherEvent.datetimeStart
                    and event.datetimeStart < otherEvent.datetimeEnd
                ):
                    availablity[otherEvent.room_id] = False
        return [{"room": room, "available": availablity[idx]} for idx, room in ROOM_LIST]

    @allowed_groups(["club", "clubs_council", "finance_council", "slo", "slc", "gad"])
    def resolve_admin_room_by_event_id(self, info, event_id):
        event = Event.objects.get(pk=event_id)
        return {
            "room": ROOM_LIST[event.room_id][1],
            "isapproved": event.room_approved,
            "population": event.population,
            "equipment": event.equipment,
            "additional": event.additional,
        }

    @allowed_groups(["club", "clubs_council", "finance_council", "slo", "slc", "gad"])
    def resolve_admin_poc_by_event_id(self, info, event_id):
        event = Event.objects.get(pk=event_id)
        return {
            "poc_name": event.poc_name,
            "poc_email": event.poc_email,
            "poc_rollno": event.poc_rollno,
            "poc_mobile": event.poc_mobile,
        }


class Mutation(graphene.ObjectType):
    new_event_description = NewEventDescription.Field()
    update_event = UpdateEvent.Field()
    update_audience = UpdateAudience.Field()

    add_room_details = AddRoomDetails.Field()
    add_poc_details = AddPocDetails.Field()
    change_poster = ChangePoster.Field()

    delete_event = DeleteEvent.Field()

    progress_event = ProgressEvent.Field()
    bypass_budget_approval = BypassBudgetApproval.Field()
    approve_cc_event = ApproveCC.Field()

    send_discussion_message = SendDiscussionMessage.Field()

    slc_reminder = SLCReminder.Field()
    slo_reminder = SLOReminder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
