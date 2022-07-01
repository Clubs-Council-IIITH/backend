from django.conf import settings
from graphene_django.types import DjangoObjectType
from finance_manager.models import BudgetRequirement


class BudgetRequirementType(DjangoObjectType):
    class Meta:
        model = BudgetRequirement
        fields = "__all__"
