from django.db import models
from django.contrib.auth.models import User as AuthUser

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
EVENT_STATES = [
    "cc_pending",
    "fc_pending",
    "slo_pending",
    "slc_pending",
    "gad_pending",
    "approved",
    "completed",
    "deleted",
]
EVENT_STATE_LIST = [ [idx, state] for idx, state in enumerate(EVENT_STATES) ]
EVENT_STATE_DICT = { state: idx for idx, state in enumerate(EVENT_STATES) }

# possible event modes
EVENT_MODE_LIST = [
    ["offline", "offline"],
    ["online", "online"],
]


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=False, null=False)
    poster = models.ImageField(upload_to="imgs/events/", blank=True, null=True)
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(default="No description available.")
    audience = models.TextField(default="none")
    datetimeStart = models.DateTimeField()
    datetimeEnd = models.DateTimeField()
    mode = models.CharField(max_length=50, choices=EVENT_MODE_LIST, default="offline")
    state = models.IntegerField(default=0, choices=EVENT_STATE_LIST, blank=False, null=False)


class EventFeedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    message = models.TextField(blank=False, null=False)
