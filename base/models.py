from auditlog.registry import auditlog
from django.db import models

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

CLUB_STATE_LIST = [["active", "ACTIVE"], ["deleted", "DELETED"]]


class Coordinator(models.Model):
    img = models.ImageField(upload_to="imgs/", blank=True)
    name = models.CharField(max_length=250)
    role = models.CharField(max_length=250, default="Coordinator")
    mail = models.EmailField()
    mobile = models.CharField(max_length=20)


class Club(models.Model):
    name = models.CharField(max_length=250)
    mail = models.EmailField()
    coordinators = models.ManyToManyField(Coordinator)
    state = models.CharField(max_length=50, choices=CLUB_STATE_LIST, default="active")


class Event(models.Model):
    name = models.CharField(max_length=250)
    last_edited_by = models.CharField(max_length=250)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)
    datetime = models.DateTimeField()
    venue = models.TextField()
    creator = models.CharField(max_length=250)
    audience = models.TextField()
    state = models.CharField(max_length=50, choices=EVENT_STATE_LIST, default="created")


auditlog.register(Event)
