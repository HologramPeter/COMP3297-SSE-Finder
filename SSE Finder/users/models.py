from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	chpStaffNumber = models.CharField(max_length=6,validators=[MinLengthValidator(6)])
	firstName = models.CharField(max_length=200)
	lastName = models.CharField(max_length=200)
	emailAddress = models.CharField(max_length=200)

	def __str__(self):
		return self.username