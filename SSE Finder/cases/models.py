from django.db import models
from demo_app.get import retrive_Data

# Create your models here.
class Infector(models.Model):
    case_number = models.IntegerField(unique=True)
    person_name = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    date_of_onset = models.DateField()
    date_of_confirmation = models.DateField()

	def __str__(self):
		return self.case_number

	def get_absolute_url(self):
		return reverse('caseInfo', args=[str(self.case_number)])

class Event(models.Model):
    infector = models.ForeignKey(Infector, on_delete=models.CASCADE)
    venue_name = models.CharField(max_length=100)
    venue_location = models.CharField(max_length=1000)
    venue_address = models.CharField(max_length=1000) # generate by function 
    venue_x_coord = models.IntegerField() # generate by function
    venue_y_coord = models.IntegerField() # generate by function 
    date_of_event = models.DateField()
    date_of_confirmation = models.DateField()
    description = models.CharField(max_length=3000)

    def save(self, *args, **kwargs):
        data = retrive_Data(self.venue_location)
        if (len(data) == 0):
            return
        else:
            self.venue_address = data[0]
            self.venue_x_coord = data[1]
            self.venue_y_coord = data[2]
        super().save(*args, **kwargs)