from base.models import Event, Club, Coordinator
from auditlog.models import LogEntry

from rest_framework import serializers

from json import loads


class LogSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source="actor.username")
    action = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = ["id", "object_pk", "event", "actor", "action", "changes", "timestamp"]

    def get_action(self, obj):
        changes = loads(obj.changes)
        if "state" in changes:
            if changes["state"][1] == "deleted":
                return 2
        return obj.action

    def get_event(self, obj):
        event = [
            {
                "name": event.name,
                "club": event.club.mail,
                "state": event.state,
                "datetime": event.datetime,
                "venue": event.venue,
                "creator": event.creator,
                "audience": event.audience,
            }
            for event in Event.objects.filter(id=int(obj.object_pk))
        ]
        return event


# Serializes club-wise roles for each Coordinator
# > Representation: [["club_id1", "role1"], ["club_id2", "role2"], ...]
# > Internal Value: "club_id1$role1,club_id2$role2, ..."
class RoleSerializer(serializers.Field):
    def to_representation(self, obj):
        return [o.split("$") for o in obj.split(",")]

    def to_internal_value(self, data):
        strs = data.replace("[", "").split("],")
        lsts = [list(map(str, s.replace("]", "").split(","))) for s in strs]
        iv = ["$".join(map(str.strip, lst)) for lst in lsts]
        return ",".join(iv).replace('"', "")


class CoordinatorSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(required=False)

    def validate_img(self, value):
        if value.size > 1048576:
            raise serializers.ValidationError("Image is too large! The maximum file size is 10MB.")
        return value

    class Meta:
        model = Coordinator
        fields = "__all__"


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"

