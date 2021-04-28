from django.contrib import admin
from cases.models import Infector, Event, Attendance
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Infector)
admin.site.register(Event)
admin.site.register(Attendance)

#add CHP number in admin view display
UserAdmin.list_display += ('CHP_staff_number',)
UserAdmin.list_filter += ('CHP_staff_number',)
UserAdmin.fieldsets[1][1]['fields'] += ('CHP_staff_number',)