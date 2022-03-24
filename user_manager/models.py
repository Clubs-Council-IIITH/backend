from datetime import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from club_manager.models import Club


class User(models.Model):
    img = models.ImageField(upload_to="imgs/users/", blank=True, null=True)
    firstName = models.CharField(max_length=250, blank=False, null=False)
    lastName = models.CharField(max_length=250, blank=False, null=False)
    mail = models.EmailField(blank=False, null=False)
    batch = models.CharField(max_length=25, blank=False, null=False)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=False, null=False)
    role = models.CharField(max_length=100)
    year = models.IntegerField(
        default=datetime.now().year,
        validators=[MaxValueValidator(3000), MinValueValidator(2000)],
    )
