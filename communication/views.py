
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from academic.forms import GradeInsertionForm, AttendenceForm, EmployeeSelectionForm
from academic.models import StudyYear, Class, Section, Subject
from .forms import SendMessageForm, TeacherMessageForm, AdvertisementForm, ParentSendMessageForm
from users.models import UserStudent, UserEmployee, Student
from .models import Message, Advertisement
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone




def send_message(request):
    user_student = UserStudent.objects.get(username=request.user.username)

    if request.method == 'POST':
        form = SendMessageForm(request.POST, request.FILES, user_student=user_student)

        if form.is_valid():
            message = form.save(commit=False)
            message.senderStudent = user_student

            # If a file was uploaded, associate it with the message
            if 'file' in request.FILES:
                message.file = request.FILES['file']

            message.save()
            # Redirect to the same page
            return HttpResponseRedirect(request.path_info)
        else:
            print(request.POST)
            print(form.errors)
    else:
        form = SendMessageForm(user_student=user_student)

    return render(request, 'communication/student_send_message.html', {'form': form})

def send_parent_message(request):
    user_parent_username = request.user.username
    user_student = UserStudent.objects.filter(parentUsername=user_parent_username).first()
    parent_full_name=user_student.student.parentFullName

    if not user_student:
        return HttpResponse("You are not authorized to send messages.")

    if request.method == 'POST':
        form = ParentSendMessageForm(request.POST, request.FILES, user_parent=user_parent_username)

        if form.is_valid():
            message = form.save(commit=False)
            message.senderParent = parent_full_name

            if 'file' in request.FILES:
                message.file = request.FILES['file']

            message.save()
            return HttpResponseRedirect(request.path_info)
        else:
            print(request.POST)
            print(form.errors)
    else:
        form = ParentSendMessageForm(user_parent=user_parent_username)

    return render(request, 'communication/parent_send_message.html', {'form': form})
def view_messages(request):
    student=UserStudent.objects.get(username=request.user.username)

    messages = Message.objects.filter(receiverStudent=student).order_by('-date')

    context = {
        'messages': messages
    }

    return render(request, 'communication/student_view_messages.html',context)


def message_details(request,message_id):
    message = get_object_or_404(Message, pk=message_id)

    context = {
        'message': message
    }

    return render(request, 'communication/student_message_details.html',context)

def parent_view_messages(request):
    student=UserStudent.objects.get(parentUsername=request.user.username)

    messages = Message.objects.filter(receiverStudent=student).order_by('-date')

    context = {
        'messages': messages
    }

    return render(request, 'communication/parent_view_messages.html',context)


def parent_message_details(request,message_id):
    message = get_object_or_404(Message, pk=message_id)

    context = {
        'message': message
    }

    return render(request, 'communication/parent_message_details.html',context)

class DownloadFileViewInsert(View):
    def get(self, request, message_id):
        message = get_object_or_404(Message, pk=message_id)

        file_path = message.file.path
        file_name = message.file.name.split('/')[-1]

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)



def teacher_view_messages(request):
    teacher = UserEmployee.objects.get(username=request.user.username)
    messages = Message.objects.filter(receiverEmployee=teacher).order_by('-date')


    context = {
        'messages': messages,
    }

    return render(request, 'communication/teacher_view_messages.html', context)

def teacher_view_message_details(request,message_id):
    message = get_object_or_404(Message, pk=message_id)

    context = {
        'message': message
    }

    return render(request, 'communication/teacher_view_message_details.html',context)


def teacher_send_message(request):
    if request.method == 'POST':
        form = GradeInsertionForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']
            # Assuming you want to filter students based on subject and possibly other criteria like year and class
            # Here's how you might adjust your query
            students = Student.objects.filter(
                studentsubject__subjectID=subject
            )

            url = reverse('communication:teacher_message_list_students', kwargs={
                'year_id': year.yearID,
                'class_id': school_class.classID,
                'section_id': section.sectionID,
                'subject_id': subject.subjectID
            })
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = GradeInsertionForm()

    return render(request, 'communication/teacher_send_message.html', {'form': form})


def teacher_message_list_students(request, year_id, class_id, section_id, subject_id):
    # Fetch the relevant objects
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)
    subject = Subject.objects.get(subjectID=subject_id)

    # Filter students
    students = Student.objects.filter(
        currentYear=year,
        currentClass=clas,
        currentSection=section,
        studentsubject__subjectID=subject
    ).order_by('fullName')  # Ensure the queryset is ordered

    # Paginate students
    paginator = Paginator(students, 5)  # Show 2 students per page
    page = request.GET.get('page')

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    context = {
        'year': year,
        'class': clas,
        'section': section,
        'subject': subject,
        'students': students
    }

    # Render the template with the provided context
    return render(request, 'communication/teacher_message_list_students.html', context)

def teacher_send_message_student(request,student_id):

    student = UserStudent.objects.get(student__studentID=student_id)


    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.senderEmployee=UserEmployee.objects.get(username=request.user.username)
            message.receiverStudent=student
            message = form.save()
    else:
        form = TeacherMessageForm()

    return render(request, 'communication/teacher_send_message_student.html', {'form': form,'student': student})

def teacher_send_message_section(request,year_id,class_id,section_id,subject_id):

    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)
    subject = Subject.objects.get(subjectID=subject_id)

    students = UserStudent.objects.filter(
        student__currentYear=year.yearID,
        student__currentClass=clas.classID,
        student__currentSection=section.sectionID,
        student__studentsubject__subjectID=subject.subjectID
    )

    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)  # Define the form here
        if form.is_valid():
            for student in students:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverStudent = student
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()  # Save each message inside the loop
    else:
        form = TeacherMessageForm()

    context = {
        'year': year,
        'class': clas,
        'section': section,
        'subject': subject,
        'form': form
    }

    return render(request, 'communication/teacher_send_message_section.html', context)


def teacher_send_message_class(request,year_id,class_id,subject_id):

    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    subject = Subject.objects.get(subjectID=subject_id)

    students = UserStudent.objects.filter(
        student__currentYear=year.yearID,
        student__currentClass=clas.classID,
        student__studentsubject__subjectID=subject.subjectID
    )

    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)  # Define the form here
        if form.is_valid():
            for student in students:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverStudent = student
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()  # Save each message inside the loop
    else:
        form = TeacherMessageForm()

    context = {
        'year': year,
        'class': clas,
        'subject': subject,
        'form': form
    }

    return render(request, 'communication/teacher_send_message_class.html', context)

def admin_view_messages(request):
    admin=UserEmployee.objects.get(username=request.user.username)

    messages = Message.objects.filter(receiverEmployee=admin).order_by('-date')

    context = {
        'messages': messages
    }

    return render(request, 'communication/admin_view_messages.html',context)

def admin_view_message_details(request,message_id):
    message = get_object_or_404(Message, pk=message_id)

    print("Sender Employee:", message.senderEmployee)
    print("Sender Student:", message.senderStudent)

    context = {
        'message': message
    }

    return render(request, 'communication/admin_view_message_details.html',context)

def secretary_view_messages(request):
    admin=UserEmployee.objects.get(username=request.user.username)

    messages = Message.objects.filter(receiverEmployee=admin).order_by('-date')

    context = {
        'messages': messages
    }

    return render(request, 'communication/secretary_view_messages.html',context)

def secretary_view_message_details(request,message_id):
    message = get_object_or_404(Message, pk=message_id)

    print("Sender Employee:", message.senderEmployee)
    print("Sender Student:", message.senderStudent)

    context = {
        'message': message
    }

    return render(request, 'communication/secretary_view_message_details.html',context)


@login_required
def admin_post_adv(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.year = StudyYear.objects.latest('yearID')  # Fetch the latest StudyYear object by yearID
            ad.date = timezone.now().date()
            ad.employee = UserEmployee.objects.get(username=request.user.username).employee
            ad.save()
    else:
        form = AdvertisementForm()
    return render(request, 'communication/admin_post_adv.html', {'form': form})

def admin_view_adv(request):
    ads = Advertisement.objects.all().order_by('-date')
    return render(request, 'communication/admin_view_adv.html', {'ads': ads})

def secretary_view_adv(request):
    ads = Advertisement.objects.all().order_by('-date')
    return render(request, 'communication/secretary_view_adv.html', {'ads': ads})

def teacher_view_adv(request):
    ads = Advertisement.objects.all().order_by('-date')
    return render(request, 'communication/teacher_view_adv.html', {'ads': ads})


def student_view_adv(request):
    ads = Advertisement.objects.all().order_by('-date')
    return render(request, 'communication/student_view_adv.html', {'ads': ads})

def parent_view_adv(request):
    ads = Advertisement.objects.all().order_by('-date')
    return render(request, 'communication/parent_view_adv.html', {'ads': ads})


def admin_send_message(request):
    if request.method == 'POST':
        form = AttendenceForm(request.POST)
        employee_form = EmployeeSelectionForm(request.POST)

        if 'submit_student' in request.POST and form.is_valid():
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']
            url = reverse('communication:admin_message_list_students', kwargs={
                'year_id': year.yearID,
                'class_id': school_class.classID,
                'section_id': section.sectionID,
            })
            return redirect(url)

        elif 'submit_employee' in request.POST and employee_form.is_valid():
            employee = employee_form.cleaned_data['employee']
            return redirect('communication:admin_send_message_employee', employee_id=employee.pk)

        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = AttendenceForm()
        employee_form = EmployeeSelectionForm()

    return render(request, 'communication/admin_send_message.html', {'form': form, 'employee_form': employee_form})

def admin_send_message_employee(request,employee_id):

    employee = UserEmployee.objects.get(employee__employeeID=employee_id)


    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.senderEmployee=UserEmployee.objects.get(username=request.user.username)
            message.receiverEmployee=employee
            message = form.save()
    else:
        form = TeacherMessageForm()

    return render(request, 'communication/admin_send_message_employee.html', {'form': form,'employee': employee})

def admin_message_list_students(request, year_id, class_id, section_id):
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)

    students = Student.objects.filter(
        currentYear=year,
        currentClass=clas,
        currentSection=section,
    ).order_by('fullName')  # Ensure the queryset is ordered

    # Pagination
    paginator = Paginator(students, 5)  # Show 20 students per page
    page = request.GET.get('page')

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    context = {
        'year': year,
        'class': clas,
        'section': section,
        'students': students
    }

    return render(request, 'communication/admin_message_list_students.html', context)

def admin_send_message_student(request,student_id):

    student = UserStudent.objects.get(student__studentID=student_id)


    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.senderEmployee=UserEmployee.objects.get(username=request.user.username)
            message.receiverStudent=student
            message = form.save()
    else:
        form = TeacherMessageForm()

    return render(request, 'communication/admin_send_message_student.html', {'form': form,'student': student})

def admin_send_message_section(request,year_id,class_id,section_id):

    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)

    students = UserStudent.objects.filter(
        student__currentYear=year.yearID,
        student__currentClass=clas.classID,
        student__currentSection=section.sectionID,
    )

    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)  # Define the form here
        if form.is_valid():
            for student in students:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverStudent = student
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()  # Save each message inside the loop
    else:
        form = TeacherMessageForm()

    context = {
        'year': year,
        'class': clas,
        'section': section,
        'form': form
    }

    return render(request, 'communication/admin_send_message_section.html', context)


def admin_send_message_class(request,year_id,class_id):

    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)

    students = UserStudent.objects.filter(
        student__currentYear=year.yearID,
        student__currentClass=clas.classID,
    )

    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)  # Define the form here
        if form.is_valid():
            for student in students:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverStudent = student
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()  # Save each message inside the loop
    else:
        form = TeacherMessageForm()

    context = {
        'year': year,
        'class': clas,
        'form': form
    }

    return render(request, 'communication/admin_send_message_class.html', context)

def admin_send_message_users(request):
    students = UserStudent.objects.all()
    employees = UserEmployee.objects.all()


    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)  # Define the form here
        if form.is_valid():
            for student in students:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverStudent = student
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()  # Save each message inside the loop
            for employee in employees:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverEmployee = employee
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()
    else:
        form = TeacherMessageForm()

    context = {
        'form': form
    }

    return render(request, 'communication/admin_send_message_users.html', context)

def admin_send_message_employees(request):
    employees = UserEmployee.objects.all()

    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)  # Define the form here
        if form.is_valid():
            for employee in employees:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverEmployee = employee
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()
    else:
        form = TeacherMessageForm()

    context = {
        'form': form
    }
    return render(request, 'communication/admin_send_message_employees.html', context)


def secretary_send_message(request):
    if request.method == 'POST':
        form = AttendenceForm(request.POST)
        employee_form = EmployeeSelectionForm(request.POST)

        if 'submit_student' in request.POST and form.is_valid():
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']
            url = reverse('communication:secretary_message_list_students', kwargs={
                'year_id': year.yearID,
                'class_id': school_class.classID,
                'section_id': section.sectionID,
            })
            return redirect(url)

        elif 'submit_employee' in request.POST and employee_form.is_valid():
            employee = employee_form.cleaned_data['employee']
            return redirect('communication:secretary_send_message_employee', employee_id=employee.pk)

        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = AttendenceForm()
        employee_form = EmployeeSelectionForm()

    return render(request, 'communication/secretary_send_message.html', {'form': form, 'employee_form': employee_form})

def secretary_send_message_employee(request,employee_id):

    employee = UserEmployee.objects.get(employee__employeeID=employee_id)


    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.senderEmployee=UserEmployee.objects.get(username=request.user.username)
            message.receiverEmployee=employee
            message = form.save()
    else:
        form = TeacherMessageForm()

    return render(request, 'communication/secretary_send_message_employee.html', {'form': form,'employee': employee})

def secretary_message_list_students(request, year_id, class_id, section_id):
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)

    students = Student.objects.filter(
        currentYear=year.yearID,
        currentClass=clas.classID,
        currentSection=section.sectionID,
    )

    context = {
        'year': year,
        'class': clas,
        'section': section,
        'students': students
    }

    # Render the template with the provided context
    return render(request, 'communication/secretary_message_list_students.html', context)

def secretary_send_message_student(request,student_id):

    student = UserStudent.objects.get(student__studentID=student_id)


    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.senderEmployee=UserEmployee.objects.get(username=request.user.username)
            message.receiverStudent=student
            message = form.save()
    else:
        form = TeacherMessageForm()

    return render(request, 'communication/secretary_send_message_student.html', {'form': form,'student': student})

def secretary_send_message_section(request,year_id,class_id,section_id):

    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)

    students = UserStudent.objects.filter(
        student__currentYear=year.yearID,
        student__currentClass=clas.classID,
        student__currentSection=section.sectionID,
    )

    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)  # Define the form here
        if form.is_valid():
            for student in students:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverStudent = student
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()  # Save each message inside the loop
    else:
        form = TeacherMessageForm()

    context = {
        'year': year,
        'class': clas,
        'section': section,
        'form': form
    }

    return render(request, 'communication/secretary_send_message_section.html', context)


def secretary_send_message_class(request,year_id,class_id):

    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)

    students = UserStudent.objects.filter(
        student__currentYear=year.yearID,
        student__currentClass=clas.classID,
    )

    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)  # Define the form here
        if form.is_valid():
            for student in students:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverStudent = student
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()  # Save each message inside the loop
    else:
        form = TeacherMessageForm()

    context = {
        'year': year,
        'class': clas,
        'form': form
    }

    return render(request, 'communication/secretary_send_message_class.html', context)

def secretary_send_message_users(request):
    students = UserStudent.objects.all()
    employees = UserEmployee.objects.all()


    if request.method == 'POST':
        form = TeacherMessageForm(request.POST, request.FILES)  # Define the form here
        if form.is_valid():
            for student in students:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverStudent = student
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()  # Save each message inside the loop
            for employee in employees:
                form_instance = TeacherMessageForm(request.POST, request.FILES)  # Create a new form instance
                message = form_instance.save(commit=False)
                message.receiverEmployee = employee
                message.senderEmployee = UserEmployee.objects.get(username=request.user.username)
                message.save()
    else:
        form = TeacherMessageForm()

    context = {
        'form': form
    }

    return render(request, 'communication/secretary_send_message_users.html', context)

