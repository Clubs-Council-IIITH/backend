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
]


class Event(models.Model):
    name = models.CharField(max_length=250)
    club = models.CharField(max_length=250)
    date = models.DateField()
    time = models.TimeField()
    venue = models.TextField()
    created_by = models.CharField(max_length=250)
    audience = MultiSelectField(choices=AUDIENCE_LIST)
    state = models.CharField(max_length=50, choices=EVENT_STATE_LIST)
