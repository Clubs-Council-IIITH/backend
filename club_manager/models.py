from django.db import models

# possible club categories
CLUB_CATEGORY_LIST = [
    ["cultural", "CULTURAL"],
    ["technical", "TECHNICAL"],
    ["other", "OTHER"],
]

# possible club states
CLUB_STATE_LIST = [
    ["active", "ACTIVE"],
    ["deleted", "DELETED"],
]


class Club(models.Model):
    img = models.ImageField(
        upload_to="imgs/clubs/", blank=True, default="/imgs/clubs/club_placeholder.jpg"
    )
    name = models.CharField(max_length=250, blank=False, null=False)
    mail = models.EmailField(blank=False, null=False)
    website = models.CharField(max_length=500, blank=True, null=True)
    category = models.CharField(
        max_length=50, choices=CLUB_CATEGORY_LIST, default="other", null=True
    )
    state = models.CharField(max_length=50, choices=CLUB_STATE_LIST, default="active", null=True)
