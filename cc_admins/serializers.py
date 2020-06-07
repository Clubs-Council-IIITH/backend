from rest_framework import serializers
from auditlog.models import LogEntry
from .models import Club


class LogSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source="actor.username")

    class Meta:
        model = LogEntry
        fields = ["id", "actor", "action", "timestamp"]


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"
