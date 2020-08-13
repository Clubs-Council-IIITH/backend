from django.db import models
from base.models import Club


class BudgetProposal(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    pdf = models.FileField(blank=True, null=True)

