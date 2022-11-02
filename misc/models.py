from django.db import models


class COC(models.Model):
    cluster = models.CharField(max_length=100)
    score = models.FloatField(default=0.0)
