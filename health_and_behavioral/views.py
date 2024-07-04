from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from academic.forms import AttendenceForm
from academic.models import StudyYear, Class, Section
from health_and_behavioral.forms import YearFilterForm, BehavioralRecord, HealthRecordForm
from health_and_behavioral.models import HealthRecord, BehaviourEvaluation
from users.models import UserStudent, Student


# Create your views here.

def view_health_records(request):
    user_student = UserStudent.objects.get(username=request.user.username)
    student = user_student.student
    health_records = HealthRecord.objects.filter(student=student)

    form_year = YearFilterForm(request.POST or None)

    if request.method == 'POST':
        if 'year' in request.POST and form_year.is_valid():
            selected_year = form_year.cleaned_data['year']
            if selected_year:
                health_records = health_records.filter(year=selected_year)

    return render(request, 'health_and_behavioral/view_health_records.html', {'user_name': request.user.username, 'health_records': health_records, 'form_year': form_year})


def view_behaviour_evaluation(request):
    user_student = UserStudent.objects.get(username=request.user.username)
    student = user_student.student
    behaviour_evaluations = BehaviourEvaluation.objects.filter(student=student)

    form_year = YearFilterForm(request.POST or None)

    if request.method == 'POST':
        if 'year' in request.POST and form_year.is_valid():
            selected_year = form_year.cleaned_data['year']
            if selected_year:
                behaviour_evaluations = behaviour_evaluations.filter(year=selected_year)

    return render(request, 'health_and_behavioral/view_behaviour_evaluation.html', {'user_name': request.user.username, 'behaviour_evaluations': behaviour_evaluations, 'form_year': form_year})

@login_required
def parent_view_health_records(request):
    try:
        user_student = UserStudent.objects.get(parentUsername=request.user.username)
        student = user_student.student
        health_records = HealthRecord.objects.filter(student=student)

        form_year = YearFilterForm(request.POST or None)

        if request.method == 'POST' and form_year.is_valid():
            selected_year = form_year.cleaned_data['year']
            if selected_year:
                health_records = health_records.filter(year=selected_year)

        return render(request, 'health_and_behavioral/parent_view_health_records.html', {
            'user_name': request.user.username,
            'health_records': health_records,
            'form_year': form_year
        })
    except UserStudent.DoesNotExist:
        return render(request, 'main_app/no_access.html')

@login_required
def parent_view_behaviour_evaluation(request):
    try:
        user_student = UserStudent.objects.get(parentUsername=request.user.username)
        student = user_student.student
        behaviour_evaluations = BehaviourEvaluation.objects.filter(student=student)

        form_year = YearFilterForm(request.POST or None)

        if request.method == 'POST' and form_year.is_valid():
            selected_year = form_year.cleaned_data['year']
            if selected_year:
                behaviour_evaluations = behaviour_evaluations.filter(year=selected_year)

        return render(request, 'health_and_behavioral/parent_view_behaviour_evaluation.html', {
            'user_name': request.user.username,
            'behaviour_evaluations': behaviour_evaluations,
            'form_year': form_year
        })
    except UserStudent.DoesNotExist:
        return render(request, 'main_app/no_access.html')

def admin_behavioral_recordI(request):
    if request.method == 'POST':
        form = AttendenceForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']

            url = reverse('health_and_behavioral:admin_behavioral_recordII',kwargs={'year_id': year.yearID, 'class_id': school_class.classID,'section_id': section.sectionID})
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = AttendenceForm()

    return render(request, 'health_and_behavioral/admin_behavioral_recordI.html', {'form': form})

def admin_behavioral_recordII(request, year_id, class_id, section_id):
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

    return render(request, 'health_and_behavioral/admin_behavioral_recordII.html', context)

def admin_behavioral_recordIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    records = BehaviourEvaluation.objects.filter(
        student=student
    ).order_by('-date')

    context = {
        'student': student,
        'records': records
    }
    return render(request, 'health_and_behavioral/admin_behavioral_recordIII.html', context)


def admin_behavioral_recordIIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = BehavioralRecord(request.POST)
        if form.is_valid():
            record = form.save(commit=False)  # Don't save yet, to set ForeignKey fields manually
            record = BehaviourEvaluation(
                year=student.currentYear,
                school_class=student.currentClass,
                section=student.currentSection,
                student=student,
                date=record.date,
                description=record.description,
                action=record.action,
                notes=record.notes,
            )
            record.save()
            url = reverse('health_and_behavioral:admin_behavioral_recordIII',
                          kwargs={'student_id': student.studentID})
            return redirect(url)
    else:
        form = BehavioralRecord()

    context = {
        'student': student,
        'form':form
    }
    return render(request, 'health_and_behavioral/admin_behavioral_recordIIII.html', context)


def admin_behavioral_record_edit(request, behavioral_id):
    behaviour_evaluation = get_object_or_404(BehaviourEvaluation, pk=behavioral_id)

    if request.method == 'POST':
        form = BehavioralRecord(request.POST, instance=behaviour_evaluation)
        if form.is_valid():
            form.save()
            url = reverse('health_and_behavioral:admin_behavioral_recordIII',
                          kwargs={'student_id': behaviour_evaluation.student.studentID})
            return redirect(url)
    else:
        form = BehavioralRecord(instance=behaviour_evaluation)  # Prepopulate the form with existing data

    return render(request, 'health_and_behavioral/admin_behavioral_record_edit.html', {'form': form})

def secretary_behavioral_recordI(request):
    if request.method == 'POST':
        form = AttendenceForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']

            url = reverse('health_and_behavioral:secretary_behavioral_recordII',kwargs={'year_id': year.yearID, 'class_id': school_class.classID,'section_id': section.sectionID})
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = AttendenceForm()

    return render(request, 'health_and_behavioral/secretary_behavioral_recordI.html', {'form': form})

def secretary_behavioral_recordII(request,year_id,class_id,section_id):

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

    return render(request, 'health_and_behavioral/secretary_behavioral_recordII.html', context)

def secretary_behavioral_recordIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    records = BehaviourEvaluation.objects.filter(
        student=student
    ).order_by('-date')

    context = {
        'student': student,
        'records': records
    }
    return render(request, 'health_and_behavioral/secretary_behavioral_recordIII.html', context)


def secretary_behavioral_recordIIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = BehavioralRecord(request.POST)
        if form.is_valid():
            record = form.save(commit=False)  # Don't save yet, to set ForeignKey fields manually
            record = BehaviourEvaluation(
                year=student.currentYear,
                school_class=student.currentClass,
                section=student.currentSection,
                student=student,
                date=record.date,
                description=record.description,
                action=record.action,
                notes=record.notes,
            )
            record.save()
            url = reverse('health_and_behavioral:secretary_behavioral_recordIII',
                          kwargs={'student_id': student.studentID})
            return redirect(url)
    else:
        form = BehavioralRecord()

    context = {
        'student': student,
        'form':form
    }
    return render(request, 'health_and_behavioral/secretary_behavioral_recordIIII.html', context)


def secretary_behavioral_record_edit(request, behavioral_id):
    behaviour_evaluation = get_object_or_404(BehaviourEvaluation, pk=behavioral_id)

    if request.method == 'POST':
        form = BehavioralRecord(request.POST, instance=behaviour_evaluation)
        if form.is_valid():
            form.save()
            url = reverse('health_and_behavioral:secretary_behavioral_recordIII',
                          kwargs={'student_id': behaviour_evaluation.student.studentID})
            return redirect(url)
    else:
        form = BehavioralRecord(instance=behaviour_evaluation)  # Prepopulate the form with existing data

    return render(request, 'health_and_behavioral/secretary_behavioral_record_edit.html', {'form': form})


def admin_health_recordI(request):
    if request.method == 'POST':
        form = AttendenceForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']

            url = reverse('health_and_behavioral:admin_health_recordII',kwargs={'year_id': year.yearID, 'class_id': school_class.classID,'section_id': section.sectionID})
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = AttendenceForm()

    return render(request, 'health_and_behavioral/admin_health_recordI.html', {'form': form})

def admin_health_recordII(request, year_id, class_id, section_id):
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

    return render(request, 'health_and_behavioral/admin_health_recordII.html', context)

def admin_health_recordIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    records = HealthRecord.objects.filter(
        student=student
    ).order_by('-date')

    context = {
        'student': student,
        'records': records
    }
    return render(request, 'health_and_behavioral/admin_health_recordIII.html', context)


def admin_health_recordIIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)  # Don't save yet, to set ForeignKey fields manually
            record = HealthRecord(
                year=student.currentYear,
                school_class=student.currentClass,
                section=student.currentSection,
                student=student,
                date=record.date,
                description=record.description,
                action=record.action,
                diagnosis=record.diagnosis,
                parentsHaveBeenContacted=record.parentsHaveBeenContacted
            )
            record.save()
            url = reverse('health_and_behavioral:admin_health_recordIII',
                          kwargs={'student_id': student.studentID})
            return redirect(url)
    else:
        form = HealthRecordForm()

    context = {
        'student': student,
        'form':form
    }
    return render(request, 'health_and_behavioral/admin_health_recordIIII.html', context)

def admin_health_record_edit(request, health_id):
    health_record = get_object_or_404(HealthRecord, pk=health_id)

    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=health_record)
        if form.is_valid():
            form.save()
            url = reverse('health_and_behavioral:admin_health_recordIII',
                          kwargs={'student_id': health_record.student.studentID})
            return redirect(url)
    else:
        form = HealthRecordForm(instance=health_record)  # Prepopulate the form with existing data

    return render(request, 'health_and_behavioral/admin_health_record_edit.html', {'form': form})


def seretary_health_recordI(request):
    if request.method == 'POST':
        form = AttendenceForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']

            url = reverse('health_and_behavioral:seretary_health_recordII',kwargs={'year_id': year.yearID, 'class_id': school_class.classID,'section_id': section.sectionID})
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = AttendenceForm()

    return render(request, 'health_and_behavioral/seretary_health_recordI.html', {'form': form})

def seretary_health_recordII(request,year_id,class_id,section_id):

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

    return render(request, 'health_and_behavioral/seretary_health_recordII.html', context)

def seretary_health_recordIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    records = HealthRecord.objects.filter(
        student=student
    ).order_by('date')

    context = {
        'student': student,
        'records': records
    }
    return render(request, 'health_and_behavioral/seretary_health_recordIII.html', context)


def seretary_health_recordIIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)  # Don't save yet, to set ForeignKey fields manually
            record = HealthRecord(
                year=student.currentYear,
                school_class=student.currentClass,
                section=student.currentSection,
                student=student,
                date=record.date,
                description=record.description,
                action=record.action,
                diagnosis=record.diagnosis,
                parentsHaveBeenContacted=record.parentsHaveBeenContacted
            )
            record.save()
            url = reverse('health_and_behavioral:seretary_health_recordIII',
                          kwargs={'student_id': student.studentID})
            return redirect(url)
    else:
        form = HealthRecordForm()

    context = {
        'student': student,
        'form':form
    }
    return render(request, 'health_and_behavioral/seretary_health_recordIIII.html', context)

def seretary_health_record_edit(request, health_id):
    health_record = get_object_or_404(HealthRecord, pk=health_id)

    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=health_record)
        if form.is_valid():
            form.save()
            url = reverse('health_and_behavioral:seretary_health_recordIII',
                          kwargs={'student_id': health_record.student.studentID})
            return redirect(url)
    else:
        form = HealthRecordForm(instance=health_record)  # Prepopulate the form with existing data

    return render(request, 'health_and_behavioral/seretary_health_record_edit.html', {'form': form})

