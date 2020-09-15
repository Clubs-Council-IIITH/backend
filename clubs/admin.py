from django.contrib import admin

from .models import EventLog, Event, Club, Coordinator

admin.site.register(EventLog)
admin.site.register(Event)
admin.site.register(Club)
admin.site.register(Coordinator)
