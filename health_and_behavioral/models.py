# health_and_behaviour/models.py

from django.db import models
from academic.models import StudyYear, Class, Section
from users.models import Student

class HealthRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    healthRecordID = models.AutoField(primary_key=True)
    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()
    parentsHaveBeenContacted = models.CharField(max_length=255)

    class Meta:
        unique_together = ('student', 'healthRecordID', 'year', 'school_class', 'section')

class BehaviourEvaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    behaviourID = models.AutoField(primary_key=True)
    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()
    notes = models.CharField(max_length=255)

    class Meta:
        unique_together = ('student', 'behaviourID', 'year', 'school_class', 'section')
