from datetime import datetime, timezone
from event_manager.models import Event, EVENT_STATES

all = 0
complete = 0
approved = 0
approved_complete = 0

for event in Event.objects.all():
    all += 1
    if event.state == 4:
        complete += 1
    elif event.state == 3:
        if event.datetimeEnd < datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=None):
            approved_complete += 1
            event.state = 4
            event.save()
        else:
            approved += 1
