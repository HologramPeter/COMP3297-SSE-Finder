from django.db import models
from cases.get import retrive_Data

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
    # infector = models.ForeignKey(Infector, on_delete=models.CASCADE)
    venue_name = models.CharField(max_length=100)
    venue_location = models.CharField(max_length=1000)
    venue_address = models.CharField(max_length=1000, blank=True, null=True) # generate by function
    venue_x_coord = models.IntegerField(blank=True, null=True) # generate by function
    venue_y_coord = models.IntegerField(blank=True, null=True) # generate by function
    date_of_event = models.DateField()
    is_SSE = models.BooleanField(default=False)
    # description = models.CharField(max_length=3000)

    def save(self, *args, **kwargs):
        print(self.venue_location)
        data = retrive_Data(self.venue_location)
        if (len(data) != 0):
            self.venue_address = data[0]
            self.venue_x_coord = data[1]
            self.venue_y_coord = data[2]
        super().save(*args, **kwargs)


class Attendance(models.Model):
    infector = models.ForeignKey(Infector, on_delete=models.CASCADE)
    event_attended = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.CharField(max_length=3000)
    is_infector = models.BooleanField() # generate by function
    is_infected = models.BooleanField() # generate by function
