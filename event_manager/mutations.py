import graphene
from graphql import GraphQLError

from django.db.models import Sum
from django.contrib.auth.models import User

from authentication.decorators import allowed_groups

from event_manager.models import Event, EVENT_STATE_DICT, ROOM_DICT, EventDiscussion
from event_manager.types import (
    ApproveCCInput,
    EventType,
    EventDiscussionType,
    EventInput,
    AudienceInput,
    RoomDetailsInput,
    ChangePosterInput,
    EventDiscussionInput,
    PocInput,
)

from club_manager.models import Club
from finance_manager.models import BudgetRequirement

from .utils import mail_notify
from datetime import timedelta


class NewEventDescription(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, _, info, event_data):
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

        # By default, the event is in the "incomplete" state,
        # once the club has added the description and the room details,
        # the event will be in the "cc_pending" state.

        event_instance.save()

        # # construct mail notification
        # mail_subject = f"Event created: '{event_data.name}'"
        # mail_body = f"{club.name} has created the event '{event_data.name}' and is waiting for your approval.\n\nLog in to clubs.iiit.ac.in to view details and add remarks."

        # # fetch all CC emails
        # cc_users = User.objects.filter(groups__name="clubs_council").all()
        # mail_to_recipients = list(map(lambda user: user.email, cc_users))

        # # send mail notification to CC
        # mail_notify(subject=mail_subject, body=mail_body, to_recipients=mail_to_recipients)

        return NewEventDescription(event=event_instance)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, _, info, event_data):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=event_data.id)

        if event_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError(
                    "You do not have permission to access this resource.")

            if event_instance.state != EVENT_STATE_DICT["incomplete"]:
                raise GraphQLError("Operation not allowed in this state.")

            if event_data.name:
                event_instance.name = event_data.name
            if event_data.datetimeStart and str(event_instance.datetimeStart + timedelta(hours=5) + timedelta(minutes=30))[:19] != str(event_data.datetimeStart):
                event_instance.datetimeStart = event_data.datetimeStart
            if event_data.datetimeEnd and str(event_instance.datetimeEnd + timedelta(hours=5) + timedelta(minutes=30))[:19] != str(event_data.datetimeEnd):
                event_instance.datetimeEnd = event_data.datetimeEnd

            # optional fields
            if event_data.audience:
                event_instance.audience = event_data.audience
            if event_data.description:
                event_instance.description = event_data.description

            # By default, the event is in the "incomplete" state,
            # once the club has added the description and the room details,
            # the event will be in the "cc_pending" state.

            # Resetting Room Data as per new details
            event_instance.room_id = 0
            event_instance.state = EVENT_STATE_DICT["incomplete"]

            event_instance.save()
            return UpdateEvent(event=event_instance)
        else:
            raise GraphQLError("Event does not exist.")

        return UpdateEvent(event=event_instance)


class UpdateAudience(graphene.Mutation):
    class Arguments:
        event_data = AudienceInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, _, info, event_data):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=event_data.id)

        if event_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError(
                    "You do not have permission to access this resource.")

            # optional fields
            if event_data.audience:
                event_instance.audience = event_data.audience

            event_instance.save()
            return UpdateAudience(event=event_instance)
        else:
            raise GraphQLError("Event does not exist.")

        return UpdateAudience(event=event_instance)


class AddRoomDetails(graphene.Mutation):
    class Arguments:
        room_data = RoomDetailsInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club", "clubs_council", "slo"])
    def mutate(cls, _, info, room_data):
        user = info.context.user
        event_instance = Event.objects.get(pk=room_data.event_id)

        if not event_instance:
            raise GraphQLError("Event does not exist.")

        if user.groups.filter(name="clubs_council").exists() or user.groups.filter(name="slo").exists():
            if room_data.room:
                event_instance.room_id = ROOM_DICT[room_data.room]

            event_instance.save()
            return AddRoomDetails(event=event_instance)

        club = Club.objects.get(mail=user.username)

        # check if event belongs to the requesting club
        if event_instance.club != club:
            raise GraphQLError(
                "You do not have permission to access this resource.")

        if room_data.room:
            event_instance.room_id = ROOM_DICT[room_data.room]
        if room_data.population:
            event_instance.population = room_data.population
        if room_data.equipment:
            event_instance.equipment = room_data.equipment
        if room_data.additional:
            event_instance.additional = room_data.additional

        event_instance.room_approved = False

        event_instance.save()
        return AddRoomDetails(event=event_instance)


class AddPocDetails(graphene.Mutation):
    class Arguments:
        poc_data = PocInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, _, info, poc_data):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=poc_data.event_id)

        if not event_instance:
            raise GraphQLError("Event does not exist.")

        # check if event belongs to the requesting club
        if event_instance.club != club:
            raise GraphQLError(
                "You do not have permission to access this resource.")

        if poc_data.poc_name:
            event_instance.poc_name = poc_data.poc_name
        if poc_data.poc_email:
            event_instance.poc_email = poc_data.poc_email
        if poc_data.poc_rollno:
            event_instance.poc_rollno = poc_data.poc_rollno
        if poc_data.poc_mobile:
            event_instance.poc_mobile = poc_data.poc_mobile

        event_instance.save()
        print(event_instance.poc_email, poc_data.poc_email)
        return AddPocDetails(event=event_instance)


class ChangePoster(graphene.Mutation):
    class Arguments:
        poster_data = ChangePosterInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, _, info, poster_data):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=poster_data.event_id)

        if not event_instance:
            raise GraphQLError("Event does not exist.")

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


class DeleteEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club", "clubs_council"])
    def mutate(cls, _, info, event_data):
        user = info.context.user
        event_instance = Event.objects.get(pk=event_data.id)

        if not event_instance:
            raise GraphQLError("Event does not exist.")

        if user.groups.filter(name="clubs_council").exists():
            event_instance.state = EVENT_STATE_DICT["deleted"]
            event_instance.room_approved = False
            event_instance.budget_approved = False

            event_instance.save()
            return DeleteEvent(event=event_instance)

        club = Club.objects.get(mail=user.username)

        # check if event belongs to the requesting club
        if event_instance.club != club:
            raise GraphQLError(
                "You do not have permission to access this resource.")

        event_instance.state = EVENT_STATE_DICT["deleted"]
        event_instance.room_approved = False
        event_instance.budget_approved = False

        event_instance.save()
        return DeleteEvent(event=event_instance)


class ApproveCC(graphene.Mutation):
    class Arguments:
        event_data = ApproveCCInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["clubs_council"])
    def mutate(cls, _, info, event_data):
        user = info.context.user
        event_instance = Event.objects.get(pk=event_data.id)

        if not event_instance:
            raise GraphQLError("Event does not exist.")

        roles = event_data.roles.split(",")
        if "none" in roles:
            event_instance.state = EVENT_STATE_DICT["approved"]
        else:
            event_instance.state = EVENT_STATE_DICT["room|budget_pending"]

        event_instance.room_approved = event_instance.budget_approved = True

        update_mail_subject = f"Event update: '{event_instance.name}'"
        update_mail_to_recipients = [event_instance.club.mail]
        update_mail_body_template = (
            "has approved the event.\n\nLog in to clubs.iiit.ac.in to view current status."
        )
        final_update_body_template = f"Your event '{event_instance.name}' has been completely approved by Clubs Council."
        approval_mail_subject = f"Event approval request: '{event_instance.name}'"
        approval_mail_body = f"{event_instance.club.name} wishes to conduct the event '{event_instance.name}' and is waiting for your approval.\n\nLog in to clubs.iiit.ac.in to view details and add remarks."

        recipients = list()
        if "slo" in roles:
            event_instance.room_approved = False
            recipients += list(map(lambda user: user.email,
                               User.objects.filter(groups__name="slo").all()))
        if "slc" in roles:
            event_instance.budget_approved = False
            recipients += list(map(lambda user: user.email,
                               User.objects.filter(groups__name="slc").all()))

        if len(recipients) >= 1:
            # send approval email to respective bodies
            mail_notify(
                subject=approval_mail_subject,
                body=approval_mail_body,
                to_recipients=recipients,
            )

            # send update mail to club
            mail_notify(
                subject=update_mail_subject,
                body=f"Clubs Council {update_mail_body_template}",
                to_recipients=update_mail_to_recipients,
            )
            print(1, recipients)
        else:
            # send update mail to club
            mail_notify(
                subject=update_mail_subject,
                body=final_update_body_template,
                to_recipients=update_mail_to_recipients,
            )

        event_instance.save()
        return ApproveCC(event=event_instance)


class ProgressEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["club", "clubs_council", "finance_council", "slo", "slc", "gad"])
    def mutate(cls, _, info, event_data):
        event_instance = Event.objects.get(pk=event_data.id)
        if not event_instance:
            raise GraphQLError("Event does not exist.")

        # construct approval mail notification
        approval_mail_subject = f"Event approval request: '{event_instance.name}'"
        approval_mail_body = f"{event_instance.club.name} wishes to conduct the event '{event_instance.name}' and is waiting for your approval.\n\nLog in to clubs.iiit.ac.in to view details and add remarks."

        # construct update mail notification
        update_mail_subject = f"Event update: '{event_instance.name}'"
        update_mail_to_recipients = [event_instance.club.mail]
        update_mail_body_template = (
            "has approved the event.\n\nLog in to clubs.iiit.ac.in to view current status."
        )

        roles = info.context.user.groups

        if event_instance.state == EVENT_STATE_DICT["incomplete"]:

            if not roles.filter(name="club").exists():
                raise GraphQLError(
                    "You do not have permission to access this resource.")

            recipients = User.objects.filter(
                groups__name="clubs_council").all()
            mail_notify(
                subject=approval_mail_subject,
                body=approval_mail_body,
                to_recipients=list(map(lambda user: user.email, recipients)),
            )
            event_instance.state = EVENT_STATE_DICT["cc_pending"]

        elif event_instance.state == EVENT_STATE_DICT["cc_pending"]:

            if not roles.filter(name="clubs_council").exists():
                raise GraphQLError(
                    "You do not have permission to access this resource.")

            # check if total budget is zero, if yes mark budget_approved as true
            # if the budget is already approved then this will not change anything
            if (
                not BudgetRequirement.objects.filter(event__pk=event_data.id).aggregate(
                    Sum("amount")
                )["amount__sum"]
            ):
                event_instance.budget_approved = True
            # check if room is not required, if yes mark room_approved as true
            # if the room is already approved then this will not change anything
            if event_instance.room_id == ROOM_DICT["none"]:
                event_instance.room_approved = True

            # bodies of whom approval is pending
            pending_bodies = []
            # if budget is still not approved, add slc to pending_bodies
            if not event_instance.budget_approved:
                pending_bodies.append("slc")
            # if room is still not approved, add slo to pending_bodies
            if not event_instance.room_approved:
                pending_bodies.append("slo")
            # send mail to all pending bodies
            for body in pending_bodies:
                recipients = User.objects.filter(groups__name=body).all()
                mail_notify(
                    subject=approval_mail_subject,
                    body=approval_mail_body,
                    to_recipients=list(
                        map(lambda user: user.email, recipients)),
                )

            # send update mail to club
            mail_notify(
                subject=update_mail_subject,
                body=f"Clubs Council {update_mail_body_template}",
                to_recipients=update_mail_to_recipients,
            )

            # if both budget and room are approved, mark event as approved
            if event_instance.budget_approved and event_instance.room_approved:
                event_instance.state = EVENT_STATE_DICT["approved"]
            else:
                event_instance.state = EVENT_STATE_DICT["room|budget_pending"]

        elif event_instance.state == EVENT_STATE_DICT["room|budget_pending"]:

            can_approve_room = (
                event_instance.room_approved == False and roles.filter(
                    name="slo").exists()
            )
            can_approve_budget = (
                event_instance.budget_approved == False and roles.filter(
                    name="slc").exists()
            )

            if not (can_approve_room or can_approve_budget):
                raise GraphQLError(
                    "You do not have permission to access this resource.")

            if can_approve_budget:
                event_instance.budget_approved = True
                # send update mail to club
                mail_notify(
                    subject=update_mail_subject,
                    body=f"Student Life Council {update_mail_body_template}",
                    to_recipients=update_mail_to_recipients,
                )
            if can_approve_room:
                event_instance.room_approved = True
                # send update mail to club
                mail_notify(
                    subject=update_mail_subject,
                    body=f"Student Life Office {update_mail_body_template}",
                    to_recipients=update_mail_to_recipients,
                )

            # if both budget and room are approved, move to next state
            if event_instance.budget_approved and event_instance.room_approved:
                event_instance.state = EVENT_STATE_DICT["approved"]
            # else, stay at the same state

        else:
            raise GraphQLError(
                "You do not have permission to access this resource.")

        event_instance.save()
        return ProgressEvent(event=event_instance)


class BypassBudgetApproval(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["clubs_council"])
    def mutate(cls, _, info, event_data):

        roles = info.context.user.groups
        if not roles.filter(name="clubs_council").exists():
            raise GraphQLError(
                "You do not have permission to access this resource.")

        event_instance = Event.objects.get(pk=event_data.id)
        if not event_instance:
            raise GraphQLError("Event does not exist.")

        event_instance.budget_approved = True

        event_instance.save()
        return BypassBudgetApproval(event=event_instance)


class SLCReminder(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["clubs_council"])
    def mutate(cls, _, info, event_data):

        roles = info.context.user.groups
        if not roles.filter(name="clubs_council").exists():
            raise GraphQLError(
                "You do not have permission to access this resource.")

        event_instance = Event.objects.get(pk=event_data.id)
        if not event_instance:
            raise GraphQLError("Event does not exist.")

        if event_instance.budget_approved == False:
            # construct approval mail notification
            approval_mail_subject = f"Waiting approval: '{event_instance.name}'"
            approval_mail_body = f"{event_instance.club.name} wishes to conduct the event '{event_instance.name}' and is waiting for your approval.\n\nRequesting you to kindly log in to clubs.iiit.ac.in to view details and add remarks."

            recipients = User.objects.filter(groups__name="slc").all()
            mail_notify(
                subject=approval_mail_subject,
                body=approval_mail_body,
                to_recipients=list(map(lambda user: user.email, recipients)),
            )

        return SLCReminder(event=event_instance)


class SLOReminder(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @classmethod
    @allowed_groups(["clubs_council"])
    def mutate(cls, _, info, event_data):

        roles = info.context.user.groups
        if not roles.filter(name="clubs_council").exists():
            raise GraphQLError(
                "You do not have permission to access this resource.")

        event_instance = Event.objects.get(pk=event_data.id)
        if not event_instance:
            raise GraphQLError("Event does not exist.")

        if event_instance.room_approved == False:
            # construct approval mail notification
            approval_mail_subject = f"Waiting approval: '{event_instance.name}'"
            approval_mail_body = f"{event_instance.club.name} wishes to conduct the event '{event_instance.name}' and is waiting for your approval.\n\nRequesting you to kindly log in to clubs.iiit.ac.in to view details and add remarks."

            recipients = User.objects.filter(groups__name="slo").all()
            mail_notify(
                subject=approval_mail_subject,
                body=approval_mail_body,
                to_recipients=list(map(lambda user: user.email, recipients)),
            )

        return SLOReminder(event=event_instance)


# TODO - Currently no emails to SLC
class SendDiscussionMessage(graphene.Mutation):
    class Arguments:
        discussion_data = EventDiscussionInput(required=True)

    discussion = graphene.Field(EventDiscussionType)

    @classmethod
    def mutate(cls, _, info, discussion_data):
        user = info.context.user
        event_instance = Event.objects.get(pk=discussion_data.event_id)

        if not event_instance:
            raise GraphQLError("Event does not exist.")

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

        if user.groups.filter(name="slc").exists() or user.groups.filter(name="slo").exists():
            # send mail notification to club
            mail_to_recipients = [event_instance.club.mail]
            mail_notify(subject=mail_subject, body=mail_body,
                        to_recipients=mail_to_recipients)

            # send mail notification to cc
            mail_to_recipients = User.objects.filter(
                groups__name="clubs_council").all()
            mail_notify(
                subject=mail_subject,
                body=mail_body,
                to_recipients=list(
                    map(lambda user: user.email, mail_to_recipients)),
            )

        if user.groups.filter(name="club").exists():
            if event_instance.room_approved == False and event_instance.state == 2:
                # send mail notification to slo
                mail_to_recipients = User.objects.filter(
                    groups__name="slo").all()
                mail_notify(
                    subject=mail_subject,
                    body=mail_body,
                    to_recipients=list(
                        map(lambda user: user.email, mail_to_recipients)),
                )

        if user.groups.filter(name="clubs_council").exists():
            if event_instance.room_approved == False and event_instance.state == 2:
                # send mail notification to slo
                mail_to_recipients = User.objects.filter(
                    groups__name="slo").all()
                mail_notify(
                    subject=mail_subject,
                    body=mail_body,
                    to_recipients=list(
                        map(lambda user: user.email, mail_to_recipients)),
                )

            # send mail notification to club
            mail_to_recipients = [event_instance.club.mail]
            mail_notify(subject=mail_subject, body=mail_body,
                        to_recipients=mail_to_recipients)

        return SendDiscussionMessage(discussion=discussion_instance)
