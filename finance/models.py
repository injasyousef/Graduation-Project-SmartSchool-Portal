# finance/models.py

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from academic.models import StudyYear, Class, Section
from users.models import Student, Employee


class ClassFee(models.Model):
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    feeAmount = models.FloatField()
    schoolUniform = models.FloatField()
    booksFee = models.FloatField()
    transports = models.FloatField()
    other = models.FloatField()



class Payments(models.Model):
    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payID = models.AutoField(primary_key=True)
    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField()
    insertedUserID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    insertingTime = models.DateTimeField()

    class Meta:
        unique_together = ('year', 'school_class', 'section', 'student', 'payID')

@receiver(post_save, sender=Payments)
def update_student_fees(sender, instance, created, **kwargs):
    if created:
        # Fetch associated StudentFees and update paid amount
        student_fees = StudentFees.objects.filter(year=instance.year, school_class=instance.school_class, section=instance.section, student=instance.student)
        for fee in student_fees:
            fee.update_paid()



class StudentFees(models.Model):
    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    schoolFees = models.FloatField(null=True, blank=True)
    paid = models.FloatField(null=True, blank=True)
    previousDebts = models.FloatField(null=True, blank=True)
    exemptions = models.FloatField()
    exemptionsDetail = models.TextField()
    finalBalance = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('year', 'school_class', 'section', 'student')

    def save(self, *args, **kwargs):
        if not self.id:
            self.initialize_data()
        super().save(*args, **kwargs)

    def initialize_data(self):
        fees = ClassFee.objects.filter(school_class=self.school_class)
        if fees.exists():
            fee = fees.first()
            self.schoolFees = fee.feeAmount + fee.schoolUniform + fee.booksFee + fee.transports + fee.other
        else:
            self.schoolFees = 0.0

        payments = Payments.objects.filter(year=self.year)
        if payments.exists():
            self.paid = sum(pay.amount for pay in payments)
        else:
            self.paid = 0.0
        prev_year = self.year.yearID - 1
        prev_debts = StudentFees.objects.filter(year__yearID=prev_year)
        if prev_debts.exists():
            self.previousDebts = sum(fee.finalBalance for fee in prev_debts)
        else:
            self.previousDebts = 0.0
        self.finalBalance = self.schoolFees - self.paid + self.previousDebts - self.exemptions

    def update_paid(self):
        payments = Payments.objects.filter(year=self.year, school_class=self.school_class, section=self.section,
                                           student=self.student)
        self.paid = sum(pay.amount for pay in payments)
        self.initialize_data()
        self.save()
