import graphene
from datetime import datetime, timedelta
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

from django.db.models import Sum
from django.contrib.auth.models import User

from authentication.decorators import allowed_groups

from event_manager.models import Event, EVENT_STATE_DICT, ROOM_DICT, EventDiscussion
from event_manager.types import EventType, EventDiscussionType

from club_manager.models import Club
from finance_manager.models import BudgetRequirement

from .utils import mail_notify


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

        # construct mail notification
        mail_subject = f"Event created: '{event_data.name}'"
        mail_body = f"{club.name} has created the event '{event_data.name}' and is waiting for your approval.\n\nLog in to clubs.iiit.ac.in to view details and add remarks."

        # fetch all CC emails
        cc_users = User.objects.filter(groups__name="clubs_council").all()
        mail_to_recipients = list(map(lambda user: user.email, cc_users))

        # send mail notification to CC
        mail_notify.delay(subject=mail_subject, body=mail_body,
                    to_recipients=mail_to_recipients)

        return CreateEvent(event=event_instance)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @ classmethod
    @ allowed_groups(["club"])
    def mutate(cls, root, info, event_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=event_data.id)

        if event_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError(
                    "You do not have permission to access this resource.")

            if not (event_instance.name == event_data.name and
                    (event_instance.datetimeStart + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S") == event_data.datetimeStart.strftime("%Y-%m-%d %H:%M:%S") and
                    (event_instance.datetimeEnd + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S") == event_data.datetimeEnd.strftime("%Y-%m-%d %H:%M:%S") and
                    event_instance.audience == event_data.audience and
                    event_instance.description == event_data.description):

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
                event_instance.state = EVENT_STATE_DICT["cc_pending"]

                event_instance.save()

                # construct mail notification
                mail_subject = f"Event updated: '{event_data.name}'"
                mail_body = f"{club.name} has updated the event '{event_data.name}' and is waiting for your approval.\n\nLog in to clubs.iiit.ac.in to view details and add remarks."

                # fetch all CC emails
                cc_users = User.objects.filter(
                    groups__name="clubs_council").all()
                mail_to_recipients = list(
                    map(lambda user: user.email, cc_users))

                # send mail notification to CC
                mail_notify.delay(subject=mail_subject, body=mail_body,
                            to_recipients=mail_to_recipients)

            return UpdateEvent(event=event_instance)

        return UpdateEvent(event=None)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @ classmethod
    @ allowed_groups(["club"])
    def mutate(cls, root, info, event_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=event_data.id)

        if event_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError(
                    "You do not have permission to access this resource.")

            event_instance.state = EVENT_STATE_DICT["deleted"]
            event_instance.room_approved = False
            event_instance.budget_approved = False

            event_instance.save()
            return DeleteEvent(event=event_instance)

        return DeleteEvent(event=event_instance)


class ProgressEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @ classmethod
    @ allowed_groups(["clubs_council", "finance_council", "slo", "slc", "gad"])
    def mutate(cls, root, info, event_data=None):
        event_instance = Event.objects.get(pk=event_data.id)

        # construct approval mail notification
        approval_mail_subject = f"Event approval request: '{event_instance.name}'"
        approval_mail_body = f"{event_instance.club.name} wishes to conduct the event '{event_instance.name}' and is waiting for your approval.\n\nLog in to clubs.iiit.ac.in to view details and add remarks."

        # construct update mail notification
        update_mail_subject = f"Event update: '{event_instance.name}'"
        update_mail_body_template = "has approved the event.\n\nLog in to clubs.iiit.ac.in to view current status."
        update_mail_to_recipients = [event_instance.club.mail]

        if event_instance:

            if event_instance.state == EVENT_STATE_DICT["cc_pending"]:
                # check if budget is not approved and total budget is non-zero, if yes progress to slc
                if event_instance.budget_approved == False and BudgetRequirement.objects.filter(event__pk=event_instance.id).aggregate(
                    Sum("amount")
                )["amount__sum"]:
                    event_instance.state = EVENT_STATE_DICT["slc_pending"]

                    # fetch all SLC emails
                    cc_users = User.objects.filter(groups__name="slc").all()
                    approval_mail_to_recipients = list(
                        map(lambda user: user.email, cc_users))

                    # send approval mail notification to SLC
                    mail_notify.delay(subject=approval_mail_subject, body=approval_mail_body,
                                to_recipients=approval_mail_to_recipients)

                # else progress to SLO
                else:
                    event_instance.state = EVENT_STATE_DICT["slo_pending"]

                    # fetch all SLO emails
                    cc_users = User.objects.filter(groups__name="slo").all()
                    approval_mail_to_recipients = list(
                        map(lambda user: user.email, cc_users))

                    # send approval mail notification to SLO
                    mail_notify.delay(subject=approval_mail_subject, body=approval_mail_body,
                                to_recipients=approval_mail_to_recipients)

                # send update mail to club
                mail_notify.delay(subject=update_mail_subject,
                            body=f"Clubs Council {update_mail_body_template}", to_recipients=update_mail_to_recipients)

            elif event_instance.state == EVENT_STATE_DICT["slc_pending"]:
                # progress to SLO
                event_instance.state = EVENT_STATE_DICT["slo_pending"]
                # set budget to approved
                event_instance.budget_approved = True

                # fetch all SLO emails
                cc_users = User.objects.filter(groups__name="slo").all()
                approval_mail_to_recipients = list(
                    map(lambda user: user.email, cc_users))

                # send approval mail notification to SLO
                mail_notify.delay(subject=approval_mail_subject, body=approval_mail_body,
                            to_recipients=approval_mail_to_recipients)

                # send update mail to club
                mail_notify.delay(subject=update_mail_subject,
                            body=f"SLC {update_mail_body_template}", to_recipients=update_mail_to_recipients)

            elif event_instance.state == EVENT_STATE_DICT["slo_pending"]:
                # check if room is not approved and room requirement is listed, if yes progress to GAD
                if event_instance.room_approved == False and event_instance.room_id != ROOM_DICT["none"]:
                    event_instance.state = EVENT_STATE_DICT["gad_pending"]

                    # fetch all SLO emails
                    cc_users = User.objects.filter(groups__name="gad").all()
                    approval_mail_to_recipients = list(
                        map(lambda user: user.email, cc_users))

                    # send approval mail notification to SLO
                    mail_notify.delay(subject=approval_mail_subject, body=approval_mail_body,
                                to_recipients=approval_mail_to_recipients)

                # else grant final approval
                else:
                    event_instance.state = EVENT_STATE_DICT["approved"]

                # send update mail to club
                mail_notify.delay(subject=update_mail_subject,
                            body=f"SLO {update_mail_body_template}", to_recipients=update_mail_to_recipients)

            elif event_instance.state == EVENT_STATE_DICT["gad_pending"]:
                # else grant final approval
                event_instance.state = EVENT_STATE_DICT["approved"]
                # set room to approved
                event_instance.room_approved = True

                # send update mail to club
                mail_notify.delay(subject=update_mail_subject,
                            body=f"GAD {update_mail_body_template}", to_recipients=update_mail_to_recipients)

            event_instance.save()
            return ProgressEvent(event=event_instance)

        return ProgressEvent(event=event_instance)


class EventDiscussionInput(graphene.InputObjectType):
    event_id = graphene.ID()
    message = graphene.String()


class SendDiscussionMessage(graphene.Mutation):
    class Arguments:
        discussion_data = EventDiscussionInput(required=True)

    discussion = graphene.Field(EventDiscussionType)

    @ classmethod
    def mutate(cls, root, info, discussion_data=None):
        user = info.context.user
        event_instance = Event.objects.get(pk=discussion_data.event_id)

        if not event_instance:
            raise GraphQLError("The target event does not exist")

        discussion_instance = EventDiscussion(
            event=event_instance,
            user=user,
            message=discussion_data.message,
        )

        discussion_instance.save()

        # construct mail notification
        mail_subject = f"Discussion: '{event_instance.name}'"
        mail_body = f"{user.first_name} sent a message on '{event_instance.name}': '{discussion_data.message}'\n\nLog in to clubs.iiit.ac.in to view the full thread and send replies."
        mail_to_recipients = [event_instance.club.mail]

        # send mail notification to club
        mail_notify.delay(subject=mail_subject, body=mail_body,
                    to_recipients=mail_to_recipients)

        return SendDiscussionMessage(discussion=discussion_instance)


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

    @ classmethod
    @ allowed_groups(["club"])
    def mutate(cls, root, info, room_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=room_data.event_id)

        if event_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError(
                    "You do not have permission to access this resource.")

            if not (event_instance.room_id == ROOM_DICT[room_data.room] and
                    (event_instance.population == room_data.population or
                    (not event_instance.population and not room_data.population)) and
                    (event_instance.equipment == room_data.equipment or
                    (not event_instance.equipment and not room_data.equipment)) and
                    (event_instance.additional == room_data.additional or
                    (not event_instance.additional and not room_data.additional))):

                if room_data.room:
                    event_instance.room_id = ROOM_DICT[room_data.room]
                if room_data.population:
                    event_instance.population = room_data.population

                event_instance.equipment = room_data.equipment
                event_instance.additional = room_data.additional

                if room_data.room == ROOM_DICT["none"]:
                    event_instance.population = 0
                    event_instance.equipment = None
                    event_instance.additional = None

                event_instance.room_approved = False
                event_instance.state = EVENT_STATE_DICT["cc_pending"]

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

    @ classmethod
    @ allowed_groups(["club"])
    def mutate(cls, root, info, poster_data):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=poster_data.event_id)

        if event_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError(
                    "You do not have permission to access this resource.")

            # if delete_prev is true then delete the previous poster
            if poster_data.delete_prev:
                event_instance.poster.delete()
            # if img is not null, set the poster as this variable
            if poster_data.img:
                event_instance.poster = poster_data.img

            event_instance.save()
            return ChangePoster(event=event_instance)

        return ChangePoster(event=None)
