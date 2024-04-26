from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Flight(models.Model):
    depature_time = models.DateTimeField()
    destination = models.CharField(max_length=200)
    available_seats = models.IntegerField()
    #  to track flights of a specific user

    def __str__(self):
        return self.destination


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} "
