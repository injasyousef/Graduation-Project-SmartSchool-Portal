from django.contrib import admin

from finance.models import ClassFee, Payments, StudentFees

# Register your models here.
admin.site.register(ClassFee)
admin.site.register(Payments)
admin.site.register(StudentFees)