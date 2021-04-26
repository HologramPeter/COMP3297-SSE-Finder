from django.contrib import admin
from cases.models import Infector, Event, Attendance

# Register your models here.
admin.site.register(Infector)
admin.site.register(Event)
admin.site.register(Attendance)
