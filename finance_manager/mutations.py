import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import superuser_required

from django.db import IntegrityError
from django.contrib.auth.models import User as AuthUser, Group

from authentication.decorators import allowed_groups

from finance_manager.models import BudgetRequirement
from finance_manager.types import BudgetRequirementType

from event_manager.models import Event, EVENT_STATE_DICT
from club_manager.models import Club


class BudgetRequirementInput(graphene.InputObjectType):
    id = graphene.ID()
    event_id = graphene.ID()
    amount = graphene.Decimal()
    description = graphene.String()
    reimbursable = graphene.Boolean()


class CreateBudgetRequirement(graphene.Mutation):
    class Arguments:
        budget_requirement_data = BudgetRequirementInput(required=True)

    budget_requirement = graphene.Field(BudgetRequirementType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, root, info, budget_requirement_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event = Event.objects.get(pk=budget_requirement_data.event_id)

        # check if event belongs to the requesting club
        if event.club != club:
            raise GraphQLError("You do not have permission to access this resource.")

        budget_requirement_instance = BudgetRequirement(
            event=event,
            amount=budget_requirement_data.amount,
            description=budget_requirement_data.description,
            reimbursable=budget_requirement_data.reimbursable,
        )

        event.budget_approved = False
        event.state = EVENT_STATE_DICT["cc_pending"]
        event.save()

        budget_requirement_instance.save()

        return CreateBudgetRequirement(budget_requirement=budget_requirement_instance)


class DeleteBudgetRequirement(graphene.Mutation):
    class Arguments:
        budget_requirement_data = BudgetRequirementInput(required=True)

    budget_requirement = graphene.Field(BudgetRequirementType)

    @classmethod
    @allowed_groups(["club"])
    def mutate(cls, root, info, budget_requirement_data=None):
        user = info.context.user
        club = Club.objects.get(mail=user.username)
        event_instance = Event.objects.get(pk=budget_requirement_data.event_id)
        budget_requirement_instance = BudgetRequirement.objects.get(pk=budget_requirement_data.id)

        if budget_requirement_instance:
            # check if event belongs to the requesting club
            if event_instance.club != club:
                raise GraphQLError("You do not have permission to access this resource.")

            event_instance.budget_approved = False
            event_instance.state = EVENT_STATE_DICT["cc_pending"]
            event_instance.save()

            budget_requirement_instance.delete()
            return DeleteBudgetRequirement(budget_requirement=None)

        return DeleteBudgetRequirement(budget_requirement=None)
