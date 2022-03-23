from graphene_django.types import DjangoObjectType
from event_manager.models import Event


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"

    def resolve_poster(self, info):
        if self.poster:
            return info.context.build_absolute_uri(self.poster.url)

        return self.poster
