from django.utils import timezone
from django.db import models

UPDATE_TAG_LIST = [["normal", "NORMAL"], ["reminder", "REMINDER"], ["important", "IMPORTANT"]]


class Update(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    datetime = models.DateTimeField(default=timezone.now, blank=False, null=False)
    creator = models.CharField(max_length=250, blank=False, null=False)
    tag = models.CharField(max_length=50, choices=UPDATE_TAG_LIST, default="normal")
