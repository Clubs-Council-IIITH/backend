from django.db import models
from multiselectfield import MultiSelectField

AUDIENCE_LIST = [
    ["none", "-"],
    ["ug1", "UG 1"],
    ["ug2", "UG 2"],
    ["ug3", "UG 3"],
    ["ugx", "UG 4+"],
    ["pg", "PG"],
    ["staff", "Staff"],
    ["faculty", "Faculty"],
]

EVENT_STATE_LIST = [
    ["created", "CREATED"],
    ["approved", "APPROVED"],
    ["published", "PUBLISHED"],
    ["scheduled", "SCHEDULED"],
    ["completed", "COMPLETED"],
    ["deleted", "DELETED"],
]


class Event(models.Model):
    name = models.CharField(max_length=250)
    user = models.CharField(max_length=250)
    datetime = models.DateTimeField()
    venue = models.TextField()
    creator = models.CharField(max_length=250)
    # audience = MultiSelectField(choices=AUDIENCE_LIST)
    state = models.CharField(max_length=50, choices=EVENT_STATE_LIST)
