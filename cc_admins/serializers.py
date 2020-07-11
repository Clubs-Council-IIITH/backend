from rest_framework import serializers
from auditlog.models import LogEntry
from base.models import Event, Club, Coordinator


class LogSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source="actor.username")
    event = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = ["id", "object_pk", "event", "actor", "action", "changes", "timestamp"]

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


class CoordinatorSerializer(serializers.ModelSerializer):
    clubs = serializers.SerializerMethodField()

    class Meta:
        model = Coordinator
        fields = "__all__"

    def get_clubs(self, obj):
        clubs = [club.name for club in Club.objects.filter(coordinators=obj.pk)]
        return clubs


class ClubSerializer(serializers.ModelSerializer):
    coordinators = CoordinatorSerializer(read_only=True, many=True)

    class Meta:
        model = Club
        fields = "__all__"
