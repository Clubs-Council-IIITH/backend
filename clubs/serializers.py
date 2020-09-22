from django.utils import timezone

from rest_framework import fields, serializers

from .models import Event, Club, Coordinator, EventLog, AUDIENCE_LIST, EVENT_STATE_LIST

from json import loads


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


class EventSerializer(serializers.ModelSerializer):
    state = fields.ChoiceField(choices=EVENT_STATE_LIST, default="created")
    club = ClubSerializer(required=False)
    last_edited_by = serializers.CharField(default=serializers.CurrentUserDefault())

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name can not be blank!")
        return value

    def validate_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event can not be in the past!")
        return value

    def validate_audience(self, value):
        key_list = set(row[0] for row in AUDIENCE_LIST)
        val_list = set(value.split(","))
        if not val_list.issubset(key_list):
            raise serializers.ValidationError("Invalid audience!")
        return value

    def validate_venue(self, value):
        if not value:
            raise serializers.ValidationError("Venue can not be blank!")
        return value

    def validate_creator(self, value):
        if not value:
            raise serializers.ValidationError("Creator can not be blank!")
        return value

    def update(self, instance, validated_data):
        instance.last_edited_by = self.context["request"].user.username
        instance.name = validated_data.get("name")
        instance.datetime = validated_data.get("datetime")
        instance.audience = validated_data.get("audience")
        instance.venue = validated_data.get("venue")
        instance.creator = validated_data.get("creator")
        instance.state = validated_data.get("state")
        instance.duration = validated_data.get("duration")
        instance.save()
        return instance

    class Meta:
        model = Event
        fields = "__all__"


class EventLogSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()

    class Meta:
        model = EventLog
        fields = "__all__"

    def get_event(self, obj):
        event = [
            {
                "name": event.name,
                "club": event.club.mail,
                "state": event.state,
                "datetime": event.datetime,
                "venue": event.venue,
                "audience": event.audience,
            }
            for event in Event.objects.filter(id=int(obj.event.id))
        ]
        return event

