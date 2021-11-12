from django.contrib import admin

# Register your models here.
from events.models import EventTypeTbl, EventsTbl

admin.site.register(EventTypeTbl)
admin.site.register(EventsTbl)