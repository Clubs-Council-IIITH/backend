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
EVENT_STATE_LIST = [
    [0, "cc_pending"],
    [1, "fc_pending"],
    [2, "gad_pending"],
    [3, "slo_pending"],
    [4, "slc_pending"],
    [5, "approved"],
    [6, "completed"],
    [7, "deleted"],
]

EVENT_STATE_DICT = {state[1]: state[0] for state in EVENT_STATE_LIST}

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
