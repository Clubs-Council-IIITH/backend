from django.db import models
from event_manager.models import Event


class BudgetRequirement(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
