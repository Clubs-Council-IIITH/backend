from django.db import models
from django.contrib.auth.models import User as AuthUser

from django.core.files import File
from PIL import Image
from io import BytesIO

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
    "slc_pending",
    "slo_pending",
    "gad_pending",
    "approved",
    "completed",
    "deleted",
]
EVENT_STATE_LIST = [[idx, state] for idx, state in enumerate(EVENT_STATES)]
EVENT_STATE_DICT = {state: idx for idx, state in enumerate(EVENT_STATES)}

# possible event modes
EVENT_MODE_LIST = [
    ["offline", "offline"],
    ["online", "online"],
]

ROOMS = [
    "none",
    # Himalaya
    "himalaya_101",
    "himalaya_102",
    "himalaya_103",
    "himalaya_104",
    "himalaya_201",
    "himalaya_202",
    "himalaya_203",
    "himalaya_204",
    "himalaya_301",
    "himalaya_302",
    "himalaya_303",
    "himalaya_304",
    # Vindhya
    "vindhya_a3_117",
    "vindhya_sh1",
    "vindhya_sh2",
    # Other
    "amphitheatre",
    "cie_gaming",
    # Academic Rooms
    "himalaya_105",
    "himalaya_205",
    "krb_auditorium",
    "ltrc_small_mr",
    "krb_faculty_mr",
    "other",
]
ROOM_LIST = [[idx, room] for idx, room in enumerate(ROOMS)]
ROOM_DICT = {room: idx for idx, room in enumerate(ROOMS)}


class Event(models.Model):
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, blank=False, null=False)
    poster = models.ImageField(upload_to="imgs/events/", blank=True, null=True)
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(default="No description available.")
    audience = models.TextField(default="none")
    datetimeStart = models.DateTimeField()
    datetimeEnd = models.DateTimeField()
    state = models.IntegerField(
        default=0, choices=EVENT_STATE_LIST, blank=False, null=False)
    room_id = models.IntegerField(
        default=0, choices=ROOM_LIST, blank=False, null=False)
    room_approved = models.BooleanField(default=False)
    budget_approved = models.BooleanField(default=False)
    population = models.IntegerField(default=0, blank=False, null=False)
    equipment = models.CharField(
        max_length=1000, default="", blank=True, null=True)
    additional = models.CharField(
        max_length=1000, default="", blank=True, null=True)
    
    def save(self, force_insert=False, force_update=False, using=None, *args, **kwargs):
        if self.poster:
            image = self.poster
            if image.size > 0.3*1024*1024:  # if size greater than 300kb then it will send to compress image function
                self.poster = compress_image(image)
        super(Event, self).save(*args, **kwargs)


class EventDiscussion(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    message = models.TextField(blank=False, null=False)


def compress_image(image):
    im = Image.open(image)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'jpeg', quality=60, optimize=True)
    new_image = File(im_io, name=image.name)
    return new_image
