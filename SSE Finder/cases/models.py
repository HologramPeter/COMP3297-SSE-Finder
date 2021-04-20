from django.db import models

# Create your models here.
class Case(models.Model):
	caseNumber = models.IntegerField()
	personName = models.CharField(max_length=200)
	idNumber = models.CharField(max_length=200)
	dateOfBirth = models.DateField()
	dateOfOnset = models.DateField()
	dateCaseConfirmed = models.DateField()
    
	def __str__(self):
		return self.caseNumber

	def get_absolute_url(self):
		return reverse('caseInfo', args=[str(self.caseNumber)])

class Event(models.Model):
	Case = models.ForeignKey(Case, on_delete=models.CASCADE)
	venueName = models.CharField(max_length=200)
	venueLocation = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	x_coord = models.FloatField()       #auto
	y_coord = models.FloatField()       #auto
	dateOfEvent = models.DateField(max_length=200)
	description = models.CharField(max_length=200)    #(informal)

	def __str__(self):
		return self.venueName