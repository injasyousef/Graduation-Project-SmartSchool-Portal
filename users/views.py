from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView

from users.decorators import login_required
from users.models import UserStudent, UserEmployee, Employee, Student


def welcome(request):
    return render(request, 'users/welcome.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import CustomLoginForm, CustomPasswordChangeForm, CustomPasswordResetForm, EmployeeForm, \
    UserEmployeeForm, StudentForm, UserStudentForm


def user_login(request):
    template_name = 'users/login.html'

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(request, template_name, {'form': form, 'error': 'Wrong username or password'})
    else:
        form = CustomLoginForm()

    return render(request, template_name, {'form': form})

def user_logout(request):
    logout(request)
    return redirect('users:login')


def view_settings(request):
    return render(request,"users/view_settings.html")

def parent_view_settings(request):
    return render(request,"users/parent_view_settings.html")

def teacher_view_settings(request):
    return render(request,"users/teacher_view_settings.html")


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def parent_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/parent_change_password.html', {'form': form})

@login_required
def teacher_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/teacher_change_password.html', {'form': form})

@login_required
def view_profile(request):
    user_student = UserStudent.objects.get(username=request.user.username)
    student = user_student.student
    return render(request, 'users/view_profile.html',{'student':student})

@login_required
def parent_view_profile(request):
    user_student = UserStudent.objects.get(parentUsername=request.user.username)
    student = user_student.student
    return render(request, 'users/parent_view_profile.html',{'student':student})


@login_required
def teacher_view_profile(request):
    user_teacher = UserEmployee.objects.get(username=request.user.username)
    teacher = user_teacher.employee
    return render(request, 'users/teacher_view_profile.html',{'teacher':teacher})

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


def admin_add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            return redirect('users:admin_add_user_employee', employee_id=employee.employeeID)
    else:
        form = EmployeeForm()
    return render(request, 'users/admin_add_employee.html', {'form': form})

def admin_add_user_employee(request, employee_id):
    employee = get_object_or_404(Employee, employeeID=employee_id)

    if request.method == 'POST':
        form = UserEmployeeForm(request.POST)
        if form.is_valid():
            user_employee = form.save(commit=False)
            user_employee.employee = employee
            try:
                user_employee.save()
                return redirect('users:admin_add_employee')  # Redirect to a success page or another view

            except forms.ValidationError as e:
                form.add_error('username', e)
    else:
        form = UserEmployeeForm()

    return render(request, 'users/admin_add_user_employee.html', {'form': form, 'employee': employee})

def admin_add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('users:admin_add_user_student', student_id=student.studentID)
    else:
        form = StudentForm()
    return render(request, 'users/admin_add_student.html', {'form': form})

def admin_add_user_student(request, student_id):
    student = get_object_or_404(Student, studentID=student_id)

    if request.method == 'POST':
        form = UserStudentForm(request.POST)
        if form.is_valid():
            user_student = form.save(commit=False)
            user_student.student = student
            try:
                user_student.save()
                return redirect('users:admin_add_student')  # Redirect to a success page or another view
            except forms.ValidationError as e:
                form.add_error(None, e)  # Add non-field error if saving fails
    else:
        form = UserStudentForm()

    return render(request, 'users/admin_add_user_student.html', {'form': form, 'student': student})

def secretary_add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('users:secretary_add_user_student', student_id=student.studentID)
    else:
        form = StudentForm()
    return render(request, 'users/secretary_add_student.html', {'form': form})

def secretary_add_user_student(request, student_id):
    student = Student.objects.get(studentID=student_id)
    if request.method == 'POST':
        form = UserStudentForm(request.POST)
        if form.is_valid():
            user_student = form.save(commit=False)  # Get an unsaved instance
            user_student.student = student  # Set the student field
            user_student.save()  # Save the instance with the student field set
            return render(request, 'users/secretary_add_user_student.html', {'form': form, 'employee': student})
    else:
        form = UserStudentForm()
    return render(request, 'users/secretary_add_user_student.html', {'form': form, 'employee': student})

def admin_view_settings(request):
    return render(request,"users/admin_view_settings.html")

@login_required
def admin_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/admin_change_password.html', {'form': form})

@login_required
def admin_view_profile(request):
    user_teacher = UserEmployee.objects.get(username=request.user.username)
    teacher = user_teacher.employee
    return render(request, 'users/admin_view_profile.html',{'teacher':teacher})

def secretary_view_settings(request):
    return render(request,"users/secretary_view_settings.html")

@login_required
def secretary_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/secretary_change_password.html', {'form': form})

@login_required
def secretary_view_profile(request):
    user_teacher = UserEmployee.objects.get(username=request.user.username)
    teacher = user_teacher.employee
    return render(request, 'users/secretary_view_profile.html',{'teacher':teacher})

