from django.db import models
from club_manager.models import Club

# possible event audiences
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

# possible event states
EVENT_STATE_LIST = [
    ["created", "CREATED"],
    ["approved", "APPROVED"],
    ["published", "PUBLISHED"],
    ["scheduled", "SCHEDULED"],
    ["completed", "COMPLETED"],
    ["deleted", "DELETED"],
]

# possible event modes
EVENT_MODE_LIST = [
    ["offline", "offline"],
    ["online", "online"],
]


class Event(models.Model):
    poster = models.ImageField(upload_to="imgs/events/", blank=True, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=False, null=False)
    datetimeStart = models.DateTimeField()
    datetimeEnd = models.DateTimeField()
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(default="No description available.")
    audience = models.TextField(default="none")
    state = models.CharField(max_length=50, choices=EVENT_STATE_LIST, default="created")
    mode = models.CharField(max_length=50, choices=EVENT_MODE_LIST, default="offline")
