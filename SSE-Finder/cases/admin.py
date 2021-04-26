from django.contrib import admin
from cases.models import Infector, Event

# Register your models here.
admin.site.register(Infector)
admin.site.register(Event)
