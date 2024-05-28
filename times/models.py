from django.db import models

class Day(models.Model):
    dayID = models.AutoField(primary_key=True)
    dayName = models.CharField(max_length=255)

    def __str__(self):
        return self.dayName

class Time(models.Model):
    timeID = models.AutoField(primary_key=True)
    hour = models.IntegerField()
    minutes = models.IntegerField()

    def __str__(self):
        return f"{self.hour}:{self.minutes}"