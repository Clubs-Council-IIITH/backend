from rest_framework import fields, serializers
from base.models import Event, AUDIENCE_LIST


class EventSerializer(serializers.ModelSerializer):
    audience = fields.MultipleChoiceField(choices=AUDIENCE_LIST)

    class Meta:
        model = Event
        fields = "__all__"
