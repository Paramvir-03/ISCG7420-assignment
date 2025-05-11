from django.db import models
from django.contrib.auth.models import User
from datetime import date, time

class ConferenceRoom(models.Model):
    name = models.CharField(max_length=100, default='Room A')
    location = models.CharField(max_length=200, default='Building 1')
    capacity = models.IntegerField(default=10)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ConferenceRoom, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    start_time = models.TimeField(default=time(9, 0))  # 9:00 AM
    end_time = models.TimeField(default=time(10, 0))   # 10:00 AM

    def __str__(self):
        return f"{self.room.name} - {self.date} ({self.start_time}-{self.end_time})"
