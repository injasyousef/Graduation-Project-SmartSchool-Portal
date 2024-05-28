from django.contrib import admin
from django.contrib.auth.models import User

from users.models import Employee, UserEmployee, Student, UserStudent

admin.site.register(Employee)
admin.site.register(UserEmployee)
admin.site.register(Student)
admin.site.register(UserStudent)



