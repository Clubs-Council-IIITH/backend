# Generated by Django 3.2.6 on 2022-07-31 06:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event_manager', '0014_rename_roomid_event_room_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventFeedback',
            new_name='EventDiscussion',
        ),
    ]