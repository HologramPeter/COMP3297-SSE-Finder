from django.db import models
from cases.get import retrive_Data

# CHP staff number
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import User

def validate_length(value,length=6):
    if len(str(value))!=length:
        raise ValidationError(u'%s is not the correct length' % value)

constraint_length_charField = models.CharField(max_length=6, validators=[validate_length], unique=True)
User.add_to_class('CHP_staff_number', constraint_length_charField)



# actual model
class Infector(models.Model):
    case_number = models.IntegerField(unique=True)
    person_name = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    date_of_onset = models.DateField()
    date_of_confirmation = models.DateField()

    def __str__(self):
        return str(self.person_name)

class Event(models.Model):
    venue_name = models.CharField(max_length=100)
    venue_location = models.CharField(max_length=1000)
    venue_address = models.CharField(max_length=1000, blank=True, null=True) # generate by function
    venue_x_coord = models.IntegerField(blank=True, null=True) # generate by function
    venue_y_coord = models.IntegerField(blank=True, null=True) # generate by function
    date_of_event = models.DateField()
    is_SSE = models.BooleanField(default=False)

    def __str__(self):
        return (self.venue_name + ', ' + self.venue_location)

class Attendance(models.Model):
    infector = models.ForeignKey(Infector, on_delete=models.CASCADE)
    event_attended = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.CharField(max_length=3000)
    is_infector = models.BooleanField() # generate by function
    is_infected = models.BooleanField() # generate by function

    def __str__(self):
        return self.description
