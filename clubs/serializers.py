from django.utils import timezone

from rest_framework import fields, serializers

from .models import Event, Club, User, Member, EventLog, AUDIENCE_LIST, EVENT_STATE_LIST

from json import loads


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField(read_only=True)

    def validate_img(self, value):
        if value.size > 1048576:
            raise serializers.ValidationError("Image is too large! The maximum file size is 10MB.")
        return value

    class Meta:
        model = User
        fields = "__all__"

    def get_roles(self, obj):
        roles = [
            {"active_year": r.active_year, "club": r.club.name, "role": r.role}
            for r in Member.objects.filter(user=obj.id)
        ]
        return roles


class MemberSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source="user", read_only=True)
    club_info = ClubSerializer(source="club", read_only=True)

    class Meta:
        model = Member
        fields = "__all__"


# TODO: clean up this mess
class EventSerializer(serializers.ModelSerializer):
    club = ClubSerializer(required=False)
    state = fields.ChoiceField(choices=EVENT_STATE_LIST, default="created")
    last_edited_by = serializers.CharField(default=serializers.CurrentUserDefault())

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
    event = EventSerializer()

    class Meta:
        model = EventLog
        fields = "__all__"

