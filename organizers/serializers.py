from rest_framework import fields, serializers
from base.models import Event, AUDIENCE_LIST, EVENT_STATE_LIST
from django.utils import timezone


class EventSerializer(serializers.ModelSerializer):
    # audience = fields.MultipleChoiceField(choices=AUDIENCE_LIST)
    state = fields.ChoiceField(choices=EVENT_STATE_LIST, default="created")
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name can not be blank!")
        return value

    def validate_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event can not be in the past!")
        return value

    def validate_venue(self, value):
        if not value:
            raise serializers.ValidationError("Venue can not be blank!")
        return value

    def validate_creator(self, value):
        if not value:
            raise serializers.ValidationError("Creator can not be blank!")
        return value

    class Meta:
        model = Event
        fields = "__all__"
