from django.utils import timezone
from django.db import models


class Update(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    datetime = models.DateTimeField(default=timezone.now, blank=False, null=False)
    creator = models.CharField(max_length=250, blank=False, null=False)
