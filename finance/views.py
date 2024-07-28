from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from academic.forms import AttendenceForm, PaymentsForm, StudentFeesForm
from academic.models import StudyYear, Class, Section
from finance.models import StudentFees, Payments
from users.models import UserStudent, Student, UserEmployee


def view_fees(request):
    user_student = UserStudent.objects.get(username=request.user.username)
    student = user_student.student
    fees = StudentFees.objects.filter(student=student)

    return render(request, "finance/view_fees.html", {"fees": fees})


def view_fee_details(request, yearID):
    user_student = UserStudent.objects.get(username=request.user.username)
    student = user_student.student
    fees = StudentFees.objects.filter(student=student)
    fee = get_object_or_404(fees, year=yearID)

    payments = Payments.objects.filter(year=yearID, student=student)
    return render(request, "finance/view_fee_details.html", {"payments": payments, "fee": fee})

def parent_view_fees(request):
    user_student = UserStudent.objects.get(parentUsername=request.user.username)
    student = user_student.student
    fees = StudentFees.objects.filter(student=student)

    return render(request, "finance/parent_view_fees.html", {"fees": fees})


def parent_view_fee_details(request, yearID):
    user_student = UserStudent.objects.get(parentUsername=request.user.username)
    student = user_student.student
    fees = StudentFees.objects.filter(student=student)
    fee = get_object_or_404(fees, year=yearID)

    payments = Payments.objects.filter(year=yearID, student=student)
    return render(request, "finance/parent_view_fee_details.html", {"payments": payments, "fee": fee})


def admin_feesI(request):
    if request.method == 'POST':
        form = AttendenceForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']

            url = reverse('finance:admin_feesII', kwargs={'year_id': year.yearID, 'class_id': school_class.classID,
                                                          'section_id': section.sectionID})
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = AttendenceForm()

    return render(request, 'finance/admin_feesI.html', {'form': form})


def admin_feesII(request, year_id, class_id, section_id):
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)

    students = Student.objects.filter(
        currentYear=year,
        currentClass=clas,
        currentSection=section,
    ).order_by('fullName')  # Ensure the queryset is ordered

    # Pagination
    paginator = Paginator(students, 10)  # Show 20 students per page
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

    return render(request, 'finance/admin_feesII.html', context)


def admin_feesIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    fee = StudentFees.objects.get(
        student=student,
        year=student.currentYear
    )

    if request.method == 'POST':
        payment_form = PaymentsForm(request.POST)
        fees_form = StudentFeesForm(request.POST, instance=fee)
        if payment_form.is_valid():
            # Access the cleaned data using the cleaned_data dictionary
            payment_data = payment_form.cleaned_data
            payment = Payments(
                year=student.currentYear,
                school_class=student.currentClass,
                section=student.currentSection,
                student=student,
                amount=payment_data['amount'],
                date=payment_data['date'],
                description=payment_data['description'],
                insertedUserID=UserEmployee.objects.get(username=request.user.username).employee,
                insertingTime=datetime.now()
            )

            payment.save()
            url = reverse('finance:admin_feesIII', kwargs={'student_id': student.studentID})
            return redirect(url)
        if fees_form.is_valid():
            fees_form.save()
            url = reverse('finance:admin_feesIII', kwargs={'student_id': student.studentID})
            return redirect(url)
    else:
        payment_form = PaymentsForm()
        fees_form = StudentFeesForm(instance=fee)

    context = {
        'student': student,
        'fee': fee,
        'payment_form': payment_form,
        'fees_form': fees_form,
    }

    return render(request, 'finance/admin_feesIII.html', context)

def admin_payments(request, student_id):
    student = get_object_or_404(Student, studentID=student_id)
    fees = StudentFees.objects.filter(student=student)
    fee = get_object_or_404(fees, year=student.currentYear)

    payments = Payments.objects.filter( student=student)
    return render(request, "finance/admin_payments.html", {"payments": payments, "fee": fee,"student":student})


def secretary_feesI(request):
    if request.method == 'POST':
        form = AttendenceForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']

            url = reverse('finance:secretary_feesII', kwargs={'year_id': year.yearID, 'class_id': school_class.classID,
                                                          'section_id': section.sectionID})
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = AttendenceForm()

    return render(request, 'finance/secretary_feesI.html', {'form': form})


def secretary_feesII(request, year_id, class_id, section_id):
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

    return render(request, 'finance/secretary_feesII.html', context)


def secretary_feesIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    fee = StudentFees.objects.get(
        student=student,
        year=student.currentYear
    )

    if request.method == 'POST':
        payment_form = PaymentsForm(request.POST)
        fees_form = StudentFeesForm(request.POST, instance=fee)
        if payment_form.is_valid():
            # Access the cleaned data using the cleaned_data dictionary
            payment_data = payment_form.cleaned_data
            payment = Payments(
                year=student.currentYear,
                school_class=student.currentClass,
                section=student.currentSection,
                student=student,
                amount=payment_data['amount'],
                date=payment_data['date'],
                description=payment_data['description'],
                insertedUserID=UserEmployee.objects.get(username=request.user.username).employee,
                insertingTime=datetime.now()
            )

            payment.save()
            url = reverse('finance:secretary_feesIII', kwargs={'student_id': student.studentID})
            return redirect(url)
        if fees_form.is_valid():
            fees_form.save()
            url = reverse('finance:secretary_feesIII', kwargs={'student_id': student.studentID})
            return redirect(url)
    else:
        payment_form = PaymentsForm()
        fees_form = StudentFeesForm(instance=fee)

    context = {
        'student': student,
        'fee': fee,
        'payment_form': payment_form,
        'fees_form': fees_form,
    }

    return render(request, 'finance/secretary_feesIII.html', context)

def secretary_payments(request, student_id):
    student = get_object_or_404(Student, studentID=student_id)
    fees = StudentFees.objects.filter(student=student)
    fee = get_object_or_404(fees, year=student.currentYear)

    payments = Payments.objects.filter( student=student)
    return render(request, "finance/secretary_payments.html", {"payments": payments, "fee": fee,"student":student})


