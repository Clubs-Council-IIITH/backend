from django.utils import timezone
from django.db import models

from base.models import Club


class BudgetProposal(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    pdf = models.FileField(blank=True, null=True)


class Update(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    datetime = models.DateTimeField(default=timezone.now, blank=False, null=False)
    creator = models.CharField(max_length=250)
