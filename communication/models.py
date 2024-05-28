# communication/models.py

from django.db import models
from users.models import UserEmployee, UserStudent


class Message(models.Model):
    messageID = models.AutoField(primary_key=True)
    title =models.CharField(max_length=255,default="")
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='messages_submit/', null=True, blank=True)
    senderEmployee = models.ForeignKey(UserEmployee, related_name='sent_messages',null=True, blank=True, on_delete=models.CASCADE)
    receiverEmployee = models.ForeignKey(UserEmployee, related_name='received_messages',null=True, blank=True, on_delete=models.CASCADE)
    senderStudent = models.ForeignKey(UserStudent, related_name='sent_messages',null=True, blank=True, on_delete=models.CASCADE)
    receiverStudent = models.ForeignKey(UserStudent, related_name='received_messages',null=True, blank=True, on_delete=models.CASCADE)

class Advertisement(models.Model):
    year = models.ForeignKey('academic.StudyYear', on_delete=models.CASCADE)
    employee = models.ForeignKey('users.Employee', on_delete=models.CASCADE)
    advertisementID = models.AutoField(primary_key=True)
    title =models.CharField(max_length=255,default="")
    content = models.TextField()
    date = models.DateField()
