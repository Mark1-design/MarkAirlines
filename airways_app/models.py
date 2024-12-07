from django.db import models
from django.contrib.auth.models import User

from datetime import date


# Create your models here.

class Appointment(models.Model):
    """ Appointment table """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    destination = models.CharField(max_length=100, null=True, blank=True)
    departure_date = models.DateField(default=date(2024, 5, 1))
    return_date = models.DateField(default=date(2024, 5, 1))
    number_of_passengers = models.IntegerField(default=1)
# To return the values in human readable format

    def __str__(self):
        return f"{self.name} - {self.destination}"
    
class Register(models.Model):
    """ Register table """
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50, default='default_password')
    confirm_password = models.CharField(max_length=10)

    def __str__(self):
        return self.username  # Fix: Return the username instead of a non-existing name field


class UploadedImage(models.Model):
    title = models.CharField(max_length=100)  #Title for the image
    image = models.ImageField(upload_to='uploaded_images') # Save images to this folder
    def __str__(self):
        return self.title     


class Booking(models.Model):
    name = models.CharField(max_length=100,default='Default Name')
    destination = models.CharField(max_length=100)
    departure_date = models.DateField(default=date(2024, 5, 1))
    return_date = models.DateField(default=date(2024, 5, 1))
    number_of_passengers = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.destination} ({self.departure_date})"