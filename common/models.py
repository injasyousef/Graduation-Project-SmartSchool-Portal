# common/models.py

from django.db import models

class City(models.Model):
    city_ID = models.AutoField(primary_key=True)
    city_Name = models.CharField(max_length=255)

    def __str__(self):
        return self.city_Name

class ParentJob(models.Model):
    parentjob_ID = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Religion(models.Model):
    religionID = models.AutoField(primary_key=True)
    religionDesc = models.CharField(max_length=255)

    def __str__(self):
        return self.religionDesc
