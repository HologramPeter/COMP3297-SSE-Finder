from django.contrib import admin
from cases.models import Infector, Event, Attendance, CHP_Staff
from django.contrib.auth.admin import UserAdmin
from django.db import models

# Register your models here.
admin.site.register(Infector)
admin.site.register(Event)
admin.site.register(Attendance)
admin.site.register(CHP_Staff, UserAdmin)

#add CHP number in admin view display
UserAdmin.list_display += ('CHP_staff_number',)
UserAdmin.list_filter += ('CHP_staff_number',)
UserAdmin.fieldsets[1][1]['fields'] += ('CHP_staff_number',)