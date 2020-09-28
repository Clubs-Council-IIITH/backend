from django.contrib import admin

from .models import EventLog, Event, Club, User, Member

admin.site.register(EventLog)
admin.site.register(Event)
admin.site.register(Club)
admin.site.register(User)
admin.site.register(Member)
