from rest_framework import serializers
from auditlog.models import LogEntry


class LogSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source="actor.username")

    class Meta:
        model = LogEntry
        fields = ["id", "actor", "action", "timestamp"]
