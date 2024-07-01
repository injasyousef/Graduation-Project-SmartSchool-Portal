# users/models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from common.models import City, ParentJob, Religion



class Employee(models.Model):
    employeeID = models.AutoField(primary_key=True)
    rule = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    secondName = models.CharField(max_length=255)
    thirdName = models.CharField(max_length=255)
    familyName = models.CharField(max_length=255)
    fullName = models.CharField(max_length=255)
    firstNameOther = models.CharField(max_length=255)
    secondNameOther = models.CharField(max_length=255)
    thirdNameOther = models.CharField(max_length=255)
    familyNameOther = models.CharField(max_length=255)
    fullNameOther = models.CharField(max_length=255)
    identificationNumber = models.IntegerField()
    empolyeeCity = models.ForeignKey(City, related_name='empolyee_city', on_delete=models.CASCADE,default=None)
    address = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    employmentDate = models.DateField()
    exitDate = models.DateField(null=True,blank=True)
    certificate = models.CharField(max_length=255)

    def __str__(self):
        return self.fullName

class UserEmployee(models.Model):
    year = models.ForeignKey('academic.StudyYear', on_delete=models.CASCADE)
    employee = models.OneToOneField(Employee, primary_key=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True)  # Ensure unique usernames
    password = models.CharField(max_length=255)
    isActive = models.BooleanField()

class Student(models.Model):
    studentID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=255)
    secondName = models.CharField(max_length=255)
    thirdName = models.CharField(max_length=255)
    familyName = models.CharField(max_length=255)
    fullName = models.CharField(max_length=255)
    firstNameOther = models.CharField(max_length=255)
    secondNameOther = models.CharField(max_length=255)
    thirdNameOther = models.CharField(max_length=255)
    familyNameOther = models.CharField(max_length=255)
    fullNameOther = models.CharField(max_length=255)
    identificationNumber = models.IntegerField()
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    birthDate = models.DateField()
    parentFullName = models.CharField(max_length=255)
    parentIdentificationNumber = models.IntegerField()
    parentCity = models.ForeignKey(City, related_name='parent_city', on_delete=models.CASCADE)
    parentAddress = models.CharField(max_length=255)
    parentPhone = models.CharField(max_length=255)
    parentEmail = models.EmailField()
    parentJob = models.ForeignKey(ParentJob, on_delete=models.CASCADE)
    motherName = models.CharField(max_length=255)
    motherPhone = models.CharField(max_length=255)
    motherIdentificationNumber = models.IntegerField()
    fatherIdentificationNumber = models.IntegerField()
    currentYear = models.ForeignKey('academic.StudyYear', related_name='current_year', on_delete=models.CASCADE)
    currentClass = models.ForeignKey('academic.Class', related_name='current_class', on_delete=models.CASCADE)
    currentSection = models.ForeignKey('academic.Section', related_name='current_section', on_delete=models.CASCADE)
    studentPhone = models.CharField(max_length=255)
    studentEmail = models.EmailField()
    numberOfFamilyMembers = models.IntegerField()
    socialStatus = models.CharField(max_length=255)
    healthStatus = models.CharField(max_length=255)

    def __str__(self):
        return self.fullName


class UserStudent(models.Model):
    year = models.ForeignKey('academic.StudyYear', on_delete=models.CASCADE)
    student = models.OneToOneField(Student, primary_key=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True)  # Ensure unique usernames
    password = models.CharField(max_length=255)
    parentUsername = models.CharField(max_length=255, unique=True)  # Ensure unique parent usernames
    parentPassword = models.CharField(max_length=255)
    isActive = models.BooleanField()
    Financialactive = models.BooleanField()

@receiver(post_save, sender=UserStudent)
def create_user_student(sender, instance, created, **kwargs):
    if created:
        student=instance.student
        emailS=student.studentEmail
        emailP=student.parentEmail
        User.objects.create_user(username=instance.username, password=instance.password,email=emailS)
        User.objects.create_user(username=instance.parentUsername, password=instance.parentPassword,email=emailP)

@receiver(post_save, sender=UserEmployee)
def create_user_employee(sender, instance, created, **kwargs):
    if created:
        emp = instance.employee
        emailE=emp.email
        User.objects.create_user(username=instance.username, password=instance.password,email=emailE)

@receiver(pre_save, sender=User)
def update_user_student_password(sender, instance, **kwargs):
    try:

        user_student = UserStudent.objects.get(username=instance.username)
    except UserStudent.DoesNotExist:

        return

    if instance.pk is not None:
        original_user = User.objects.get(pk=instance.pk)
        if original_user.password != instance.password:
            user_student.password = instance.password
            user_student.save()


