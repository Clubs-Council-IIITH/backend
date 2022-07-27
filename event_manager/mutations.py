import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

from django.db.models import Sum

from authentication.decorators import allowed_groups

from event_manager.models import Event, EVENT_STATE_DICT, ROOM_DICT, EventFeedback
from event_manager.types import EventType, EventFeedbackType

from club_manager.models import Club
from finance_manager.models import BudgetRequirement


class EventInput(graphene.InputObjectType):
    id = graphene.ID()
    datetimeStart = graphene.DateTime()
    datetimeEnd = graphene.DateTime()
    name = graphene.String()
    description = graphene.String()
    audience = graphene.String()


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
        )

        # optional fields
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

            # optional fields
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

            event_instance.state = EVENT_STATE_DICT["deleted"]
            event_instance.save()
            return DeleteEvent(event=event_instance)

        return DeleteEvent(event=event_instance)


class ProgressEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["clubs_council", "finance_council", "slo", "slc", "gad"])
    def mutate(cls, root, info, event_data=None):
        event_instance = Event.objects.get(pk=event_data.id)

        if event_instance:

            if event_instance.state == EVENT_STATE_DICT["cc_pending"]:
                # check if total budget is non-zero, if yes progress to FC
                if BudgetRequirement.objects.filter(event__pk=event_instance.id).aggregate(
                    Sum("amount")
                )["amount__sum"]:
                    event_instance.state = EVENT_STATE_DICT["fc_pending"]
                # else progress to SLO
                else:
                    event_instance.state = EVENT_STATE_DICT["slo_pending"]

            elif event_instance.state == EVENT_STATE_DICT["fc_pending"]:
                # progress to SLO
                event_instance.state = EVENT_STATE_DICT["slo_pending"]

            elif event_instance.state == EVENT_STATE_DICT["slo_pending"]:
                # progress to SLC
                event_instance.state = EVENT_STATE_DICT["slc_pending"]

            elif event_instance.state == EVENT_STATE_DICT["slc_pending"]:
                # check if room requirement is listed, if yes progress to GAD
                if event_instance.room_id != ROOM_DICT["none"]:
                    event_instance.state = EVENT_STATE_DICT["gad_pending"]
                # else grant final approval
                else:
                    event_instance.state = EVENT_STATE_DICT["approved"]

            elif event_instance.state == EVENT_STATE_DICT["gad_pending"]:
                # else grant final approval
                event_instance.state = EVENT_STATE_DICT["approved"]

            event_instance.save()
            return ProgressEvent(event=event_instance)

        return ProgressEvent(event=event_instance)


class EventFeedbackInput(graphene.InputObjectType):
    event_id = graphene.ID()
    message = graphene.String()


class AddEventFeedback(graphene.Mutation):
    class Arguments:
        feedback_data = EventFeedbackInput(required=True)

    feedback = graphene.Field(EventFeedbackType)

    @classmethod
    def mutate(cls, root, info, feedback_data=None):
        user = info.context.user
        event_instance = Event.objects.get(pk=feedback_data.event_id)

        if not event_instance:
            raise GraphQLError("The target event does not exist")

        feedback_instance = EventFeedback(
            event=event_instance,
            user=user,
            message=feedback_data.message,
        )

        feedback_instance.save()

        return AddEventFeedback(feedback=feedback_instance)


class RoomDetailsInput(graphene.InputObjectType):
    event_id = graphene.ID()
    room = graphene.String()
    population = graphene.Int()
    equipment = graphene.String(required=False)
    additional = graphene.String(required=False)


class AddRoomDetails(graphene.Mutation):
    class Arguments:
        room_data = RoomDetailsInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, root, info, room_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=room_data.event_id)

        if event_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError("You do not have permission to access this resource.")

            if room_data.room:
                event_instance.room_id = ROOM_DICT[room_data.room]
            if room_data.population:
                event_instance.population = room_data.population
            if room_data.equipment:
                event_instance.equipment = room_data.equipment
            if room_data.additional:
                event_instance.additional = room_data.additional

            event_instance.save()
            return AddRoomDetails(event=event_instance)

        return AddRoomDetails(event=None)


class ChangePosterInput(graphene.InputObjectType):
    event_id = graphene.ID()
    img = Upload(required=False)
    delete_prev = graphene.Boolean()


class ChangePoster(graphene.Mutation):
    class Arguments:
        poster_data = ChangePosterInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, root, info, poster_data):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=poster_data.event_id)

        if event_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError("You do not have permission to access this resource.")

            # if delete_prev is true then delete the previous poster
            if poster_data.delete_prev:
                event_instance.poster.delete()
            # if img is not null, set the poster as this variable
            if poster_data.img:
                event_instance.poster = poster_data.img

            event_instance.save()
            return ChangePoster(event=event_instance)

        return ChangePoster(event=None)
