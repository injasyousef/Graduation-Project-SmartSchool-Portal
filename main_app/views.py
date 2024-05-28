from django.shortcuts import render

# main_app/views.py
from django.shortcuts import render
from users.decorators import login_required
from users.models import UserStudent,UserEmployee

@login_required
def home_page(request):
    try:
        # Check if the user is a student
        user_student = UserStudent.objects.get(username=request.user.username)
        student = user_student.student
        user_name = student.firstName
        return render(request, 'main_app/student_page.html', {"user_name": user_name})
    except UserStudent.DoesNotExist:
        try:
            # Check if the user is an employee
            user_emp = UserEmployee.objects.get(username=request.user.username)
            emp = user_emp.employee
            if emp.rule == 'teacher':
                return render(request, 'main_app/teacher_page.html')
            elif emp.rule == 'admin':
                return render(request, 'main_app/admin_page.html')
            elif emp.rule == 'secretary':
                return render(request, 'main_app/secretary_page.html')
        except UserEmployee.DoesNotExist:
            # Check if the user is a parent
            user_student = UserStudent.objects.get(parentUsername=request.user.username)
            student = user_student.student
            return render(request, 'main_app/parent_page.html', {"student": student})
