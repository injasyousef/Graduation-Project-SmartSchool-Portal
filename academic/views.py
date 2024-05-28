from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, FileResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View

from health_and_behavioral.models import BehaviourEvaluation
from times.models import Day, Time
from users.forms import StudentForm, EmployeeForm
from .forms import YearFilterForm, SubjectFilterForm, AttendanceYearFilterForm, AssignmentSubmissionForm, \
    GradeInsertionForm, NewAssForm, AssignmentForm, AssignmentGradeUpdateForm, ExamForm, ExamGradeUpdateForm, \
    AttendenceForm, AttendanceRecordForm, ClassForm, SectionForm, SubjectForm, ClassSubjectForm, StudyYearForm, \
    SchoolSittingsForm, StudentSelection, EmployeeSelectionForm
from .models import Grade, Attendance, Assignment, Lecture, Subject, Class, ClassSubject, StudyYear, Section, Exam, \
    SchoolSittings, StudentSubject
from users.models import UserStudent, Student, UserEmployee, Employee
from datetime import datetime, timedelta
import datetime as dt
from django.shortcuts import redirect
from django.urls import reverse


def base_view_grades(request):
    user_student = UserStudent.objects.get(username=request.user.username)
    student = user_student.student
    grades = Grade.objects.filter(student=student)

    form_subject = SubjectFilterForm(request.POST or None)
    form_year = YearFilterForm(request.POST or None)

    if request.method == 'POST':
        if 'subject' in request.POST and form_subject.is_valid():
            selected_subject = form_subject.cleaned_data['subject']
            if selected_subject:
                grades = grades.filter(subject=selected_subject)

        if 'year' in request.POST and form_year.is_valid():
            selected_year = form_year.cleaned_data['year']
            if selected_year:
                grades = grades.filter(year=selected_year)

    return render(request, 'academic/base_view_grades.html',
                  {'user_name': request.user.username, 'grades': grades, 'form_subject': form_subject,
                   'form_year': form_year})

@login_required
def parent_view_grades(request):
    try:
        # Retrieve the student based on the parent's username
        user_student = UserStudent.objects.get(parentUsername=request.user.username)
        student = user_student.student
        grades = Grade.objects.filter(student=student)

        form_subject = SubjectFilterForm(request.POST or None)
        form_year = YearFilterForm(request.POST or None)

        if request.method == 'POST':
            if 'subject' in request.POST and form_subject.is_valid():
                selected_subject = form_subject.cleaned_data['subject']
                if selected_subject:
                    grades = grades.filter(subject=selected_subject)

            if 'year' in request.POST and form_year.is_valid():
                selected_year = form_year.cleaned_data['year']
                if selected_year:
                    grades = grades.filter(year=selected_year)

        return render(request, 'academic/parent_view_grades.html', {
            'user_name': request.user.username,
            'grades': grades,
            'form_subject': form_subject,
            'form_year': form_year
        })
    except ObjectDoesNotExist:
        return render(request, 'main_app/no_access.html')


def view_attendance(request):
    user_student = UserStudent.objects.get(username=request.user.username)
    student = user_student.student
    attendance_history = Attendance.objects.filter(student=student)

    form_year = AttendanceYearFilterForm(request.POST or None)

    if request.method == 'POST':
        if 'year' in request.POST and form_year.is_valid():
            selected_year = form_year.cleaned_data['year']
            if selected_year:
                attendance_history = attendance_history.filter(year=selected_year)

    return render(request, 'academic/view_attendance.html',
                  {'user_name': request.user.username, 'attendance_history': attendance_history,
                   'form_year': form_year})

def parent_view_attendance(request):
    user_student = UserStudent.objects.get(parentUsername=request.user.username)
    student = user_student.student
    attendance_history = Attendance.objects.filter(student=student)

    form_year = AttendanceYearFilterForm(request.POST or None)

    if request.method == 'POST':
        if 'year' in request.POST and form_year.is_valid():
            selected_year = form_year.cleaned_data['year']
            if selected_year:
                attendance_history = attendance_history.filter(year=selected_year)

    return render(request, 'academic/parent_view_attendance.html',
                  {'user_name': request.user.username, 'attendance_history': attendance_history,
                   'form_year': form_year})


def see_assignments(request):
    user_name = request.user.username
    user_student = UserStudent.objects.get(username=request.user.username)
    student = user_student.student
    assignments = Assignment.objects.filter(student=student).order_by("-dueDate")
    selected_year = None

    if request.method == 'POST':
        form = YearFilterForm(request.POST)
        if form.is_valid():
            selected_year = form.cleaned_data['year']
            if selected_year:
                assignments = assignments.filter(year=selected_year)

    form = YearFilterForm()
    threshold_date = datetime.now().date()

    return render(request, 'academic/see_assignments.html',
                  {'form': form, 'assignments': assignments, 'user_name': user_name, 'selected_year': selected_year,
                   'threshold_date': threshold_date})

def parent_view_assignments(request):
    user_name = request.user.username
    user_student = UserStudent.objects.get(parentUsername=request.user.username)
    student = user_student.student
    assignments = Assignment.objects.filter(student=student)
    selected_year = None

    if request.method == 'POST':
        form = YearFilterForm(request.POST)
        if form.is_valid():
            selected_year = form.cleaned_data['year']
            if selected_year:
                assignments = assignments.filter(year=selected_year)

    form = YearFilterForm()
    threshold_date = datetime.now().date()

    return render(request, 'academic/parent_view_assignments.html',
                  {'form': form, 'assignments': assignments, 'user_name': user_name, 'selected_year': selected_year,
                   'threshold_date': threshold_date})


def view_exams(request):
    user_name = request.user.username
    user_student = UserStudent.objects.get(username=request.user.username)
    student = user_student.student
    exams = Exam.objects.filter(student=student).order_by("-date")

    form_subject = SubjectFilterForm(request.POST or None)

    if request.method == 'POST':
        if 'subject' in request.POST and form_subject.is_valid():
            selected_subject = form_subject.cleaned_data['subject']
            if selected_subject:
                exams = exams.filter(subject=selected_subject)

    return render(request, 'academic/view_exams.html',
                  {'exams': exams, 'user_name': user_name, 'form_subject': form_subject})

def parent_view_exams(request):
    user_name = request.user.username
    user_student = UserStudent.objects.get(parentUsername=request.user.username)
    student = user_student.student
    exams = Exam.objects.filter(student=student)

    form_subject = SubjectFilterForm(request.POST or None)

    if request.method == 'POST':
        if 'subject' in request.POST and form_subject.is_valid():
            selected_subject = form_subject.cleaned_data['subject']
            if selected_subject:
                exams = exams.filter(subject=selected_subject)

    return render(request, 'academic/parent_view_exams.html',
                  {'exams': exams, 'user_name': user_name, 'form_subject': form_subject})


from django.utils import timezone


def view_assignment_details(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    today = timezone.now().date()
    flag = True

    if assignment.dueDate < today:

        form = AssignmentSubmissionForm(instance=assignment)
        form.fields['fileSubmit'].widget.attrs['disabled'] = True
        form.fields['link'].widget.attrs['disabled'] = True
        form.fields['submit_text'].widget.attrs['disabled'] = True
        flag = False
    else:

        if request.method == 'POST':
            form = AssignmentSubmissionForm(request.POST, request.FILES, instance=assignment)
            if form.is_valid():

                if 'clear_file_submit' in request.POST:
                    form.instance.fileSubmit = None

                assignment = form.save(commit=False)
                if assignment.submit_text or assignment.fileSubmit or assignment.link:
                    assignment.submit = True
                else:
                    assignment.submit = False
                assignment.save()
                return redirect('academic:see_assignments')
        else:
            form = AssignmentSubmissionForm(instance=assignment)

    return render(request, 'academic/view_assignment_details.html',
                  {'assignment': assignment, 'form': form, 'today': today, 'flag': flag})


def view_weekly_schedule(request):
    days = Day.objects.all()
    schedule_hours = Time.objects.all()
    user_student = UserStudent.objects.get(username=request.user.username)
    current_class = user_student.student.currentClass

    lectures = Lecture.objects.filter(classID=current_class)

    return render(request, 'academic/view_weekly_schedule.html',
                  {'lectures': lectures, 'days': days, 'schedule_hours': schedule_hours})


def view_lecture_details(request, lectureID):
    lecture = get_object_or_404(Lecture, pk=lectureID)

    return render(request, 'academic/view_lecture_details.html', {'lecture': lecture})

def parent_view_weekly_schedule(request):
    days = Day.objects.all()
    schedule_hours = Time.objects.all()
    user_student = UserStudent.objects.get(parentUsername=request.user.username)
    current_class = user_student.student.currentClass

    lectures = Lecture.objects.filter(classID=current_class)

    return render(request, 'academic/parent_view_weekly_schedule.html',
                  {'lectures': lectures, 'days': days, 'schedule_hours': schedule_hours})


def parent_view_lecture_details(request, lectureID):
    lecture = get_object_or_404(Lecture, pk=lectureID)

    return render(request, 'academic/parent_view_lecture_details.html', {'lecture': lecture})



class DownloadFileView(View):
    def get(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, pk=assignment_id)

        file_path = assignment.fileSubmit.path
        file_name = assignment.fileSubmit.name.split('/')[-1]
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)


class DownloadFileViewInsert(View):
    def get(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, pk=assignment_id)

        file_path = assignment.fileInsert.path
        file_name = assignment.fileInsert.name.split('/')[-1]

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)


class DownloadFileSubmited(View):
    def get(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, pk=assignment_id)

        file_path = assignment.fileSubmit.path
        file_name = assignment.fileSubmit.name.split('/')[-1]

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)


def teacher_insert_grades(request):
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

            # Your existing logic for handling valid form submissions follows...
            url = reverse('academic:list_student')
            url += f'?year={year.yearID}&class={school_class.classID}&section={section.sectionID}&subject={subject.subjectID}'
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = GradeInsertionForm()

    return render(request, 'academic/teacher_insert_grades.html', {'form': form})


def get_classes_for_year(request):
    year_id = request.GET.get('year_id')
    class_subjects = ClassSubject.objects.filter(year_id=year_id).select_related('school_class').distinct()
    classes = {cs.school_class for cs in class_subjects}
    class_list = [{'id': cls.classID, 'name': cls.className} for cls in classes]
    return JsonResponse(class_list, safe=False)


def get_sections_for_class_and_year(request):
    year_id = request.GET.get('year_id')
    class_id = request.GET.get('class_id')
    try:
        sections = Section.objects.filter(
            year_id=year_id,
            school_class_id=class_id
        ).order_by('sectionSymbol')
        section_list = [{'id': section.sectionID, 'symbol': section.sectionSymbol} for section in sections]
        return JsonResponse(section_list, safe=False)
    except Exception as e:
        print(f"Error in get_sections_for_class_and_year: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)


def get_students_for_class_section_and_year(request):
    year_id = request.GET.get('year_id')
    class_id = request.GET.get('class_id')
    section_id = request.GET.get('section_id')
    try:
        students = Student.objects.filter(
            currentYear_id=year_id,
            currentClass_id=class_id,
            currentSection_id=section_id
        )
        student_list = [{'id': student.studentID, 'name': student.fullName} for student in students]
        return JsonResponse(student_list, safe=False)
    except Exception as e:
        print(f"Error in get_students_for_class_section_and_year: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)


def get_subjects_for_section(request):
    year_id = request.GET.get('year_id')
    class_id = request.GET.get('class_id')
    section_id = request.GET.get('section_id')
    try:
        # Assuming ClassSubject links subjects to sections indirectly through class and year,
        # and there's a way to filter subjects for a specific section.
        subjects = Subject.objects.filter(
            classsubject__year_id=year_id,
            classsubject__school_class_id=class_id,
            classsubject__teacher_id=UserEmployee.objects.get(username=request.user.username).employee.employeeID,
            # If ClassSubject actually contains a section reference, uncomment the next line
            # classsubject__section_id=section_id
        ).distinct().order_by('name')

        subject_list = [{'id': subject.subjectID, 'name': subject.name} for subject in subjects]
        return JsonResponse(subject_list, safe=False)
    except Exception as e:
        print(f"Error in get_subjects_for_section: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)


def get_subjects_for_class(request):
    year_id = request.GET.get('year_id')
    class_id = request.GET.get('class_id')
    try:
        # Assuming ClassSubject links subjects to sections indirectly through class and year,
        # and there's a way to filter subjects for a specific section.
        subjects = Subject.objects.filter(
            classsubject__year_id=year_id,
            classsubject__school_class_id=class_id,
            # If ClassSubject actually contains a section reference, uncomment the next line
            # classsubject__section_id=section_id
        ).distinct().order_by('name')
        subject_list = [{'id': subject.subjectID, 'name': subject.name} for subject in subjects]
        return JsonResponse(subject_list, safe=False)
    except Exception as e:
        print(f"Error in get_subjects_for_section: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)


def list_student(request):
    # Retrieve the passed parameters from the URL query string
    year_id = request.GET.get('year')
    class_id = request.GET.get('class')
    section_id = request.GET.get('section')
    subject_id = request.GET.get('subject')

    # You can perform any additional logic here, such as fetching related objects or data

    # Example: Fetching the names of the selected objects (you'll need appropriate models and relationships)
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)
    subject = Subject.objects.get(subjectID=subject_id)

    students = Student.objects.filter(
        currentYear=year.yearID,
        currentClass=clas.classID,
        currentSection=section.sectionID,
        studentsubject__subjectID=subject.subjectID
    )

    # Pass the retrieved data to the template
    context = {
        'students': students,
        'year_id': year.yearID,
        'class_id': clas.classID,
        'section_id': section.sectionID,
        'subject_id': subject.subjectID,
    }

    # Render the template with the provided context
    return render(request, 'academic/list_student.html', context)


def student_grade(request, student_id, year_id, class_id, section_id, subject_id):
    # Retrieve the student and related attributes
    student = get_object_or_404(Student, pk=student_id)
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)
    subject = Subject.objects.get(subjectID=subject_id)

    try:
        grade = Grade.objects.get(
            student=student,
            year=year,
            school_class=clas,
            section=section,
            subject=subject
        )
    except Grade.DoesNotExist:
        grade = None

    if request.method == 'POST':
        # Process form data
        firstQuarter = request.POST.get('firstQuarter', None)
        secondQuarter = request.POST.get('secondQuarter', None)
        thirdQuarter = request.POST.get('thirdQuarter', None)
        fourthQuarter = request.POST.get('fourthQuarter', None)

        # Update the existing record only if the form field has a valid value
        if grade:
            if firstQuarter:
                grade.firstQuarter = float(firstQuarter)
            if secondQuarter:
                grade.secondQuarter = float(secondQuarter)
            if thirdQuarter:
                grade.thirdQuarter = float(thirdQuarter)
            if fourthQuarter:
                grade.fourthQuarter = float(fourthQuarter)
            grade.save()
        else:
            # If grade does not exist, create a new record only if at least one form field has a valid value
            if firstQuarter or secondQuarter or thirdQuarter or fourthQuarter:
                grade = Grade.objects.create(
                    student=student,
                    year=year,
                    school_class=clas,
                    section=section,
                    subject=subject,
                    firstQuarter=float(firstQuarter) if firstQuarter else None,
                    secondQuarter=float(secondQuarter) if secondQuarter else None,
                    thirdQuarter=float(thirdQuarter) if thirdQuarter else None,
                    fourthQuarter=float(fourthQuarter) if fourthQuarter else None,
                    teacher=UserEmployee.objects.get(username=request.user.username).employee
                )

        # Redirect to the same page after processing the form
        return redirect('academic:student_grade', student_id=student_id, year_id=year_id, class_id=class_id,
                        section_id=section_id, subject_id=subject_id)

    # Pass the retrieved data to the template
    context = {
        'student': student,
        'grade': grade,
        'year_name': year.yearName,
        'class_name': clas.className,
        'section_symbol': section.sectionSymbol,
        'subject_name': subject.name,
    }

    # Render the template with the provided context
    return render(request, 'academic/student_grade.html', context)


def teacher_new_assignment(request):
    if request.method == 'POST':
        form = GradeInsertionForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']
            # Your existing logic for handling valid form submissions follows...
            url = reverse('academic:teacher_add_new_assignment')
            url += f'?year={year.yearID}&class={school_class.classID}&section={section.sectionID}&subject={subject.subjectID}'
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = GradeInsertionForm()

    return render(request, 'academic/teacher_new_assignment.html', {'form': form})


def teacher_add_new_assignment(request):
    global form
    year_id = request.GET.get('year')
    class_id = request.GET.get('class')
    subject_id = request.GET.get('subject')
    section_id = request.GET.get('section')

    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    subject = Subject.objects.get(subjectID=subject_id)
    section = Section.objects.get(sectionID=section_id)

    students = Student.objects.filter(
        currentYear=year.yearID,
        currentClass=clas.classID,
        currentSection=section.sectionID,
        studentsubject__subjectID=subject.subjectID
    )

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment_data = form.save(commit=False)  # Save the form data without committing to the database
            for student in students:
                # Create a new Assignment object for each student
                assignment = Assignment(
                    title=assignment_data.title,
                    description=assignment_data.description,
                    dueDate=assignment_data.dueDate,
                    fileInsert=assignment_data.fileInsert,
                    teacher=UserEmployee.objects.get(username=request.user.username).employee,
                    subject=subject,
                    linkInsert=assignment_data.linkInsert,
                    student=student,
                    year=student.currentYear,
                    school_class=student.currentClass,
                    section=student.currentSection
                )
                assignment.save()  # Save the new assignment record

            success_message = "Assignments have been successfully added."
    else:
        form = AssignmentForm()
    context = {
        'year': year,
        'class': clas,
        'subject': subject,
        'students': students,  # Pass the list of students to the context
        'section': section,
        'form': form

    }

    # Render the template with the provided context
    return render(request, 'academic/teacher_add_new_assignment.html', context)


def teacher_view_assignments(request):
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

            # Your existing logic for handling valid form submissions follows...
            url = reverse('academic:list_students_for_assignments')
            url += f'?year={year.yearID}&class={school_class.classID}&section={section.sectionID}&subject={subject.subjectID}'
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = GradeInsertionForm()

    return render(request, 'academic/teacher_view_assignments.html', {'form': form})


def list_students_for_assignments(request):
    # Retrieve the passed parameters from the URL query string
    year_id = request.GET.get('year')
    class_id = request.GET.get('class')
    section_id = request.GET.get('section')
    subject_id = request.GET.get('subject')

    # You can perform any additional logic here, such as fetching related objects or data

    # Example: Fetching the names of the selected objects (you'll need appropriate models and relationships)
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)
    subject = Subject.objects.get(subjectID=subject_id)

    students = Student.objects.filter(
        currentYear=year.yearID,
        currentClass=clas.classID,
        currentSection=section.sectionID,
        studentsubject__subjectID=subject.subjectID
    )

    # Pass the retrieved data to the template
    context = {
        'students': students,
        'year_id': year.yearID,
        'class_id': clas.classID,
        'section_id': section.sectionID,
        'subject_id': subject.subjectID,
    }

    # Render the template with the provided context
    return render(request, 'academic/list_students_for_assignments.html', context)


def assignments_for_student(request, student_id, year_id, class_id, section_id, subject_id):
    student = get_object_or_404(Student, pk=student_id)
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)
    subject = Subject.objects.get(subjectID=subject_id)

    assignments = Assignment.objects.filter(
        year=year,
        school_class=clas,
        section=section,
        subject=subject,
        student=student,
        teacher=UserEmployee.objects.get(username=request.user.username).employee
    ).order_by("-dueDate")

    context = {
        'student': student,
        'year': year,
        'class': clas,
        'section': section,
        'subject': subject,
        'assignments': assignments
    }

    # Render the template with the provided context
    return render(request, 'academic/assignments_for_student.html', context)


def assignment_grading(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == 'POST':
        form = AssignmentGradeUpdateForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            # Redirect or render success message
    else:
        form = AssignmentGradeUpdateForm(instance=assignment)

    context = {
        'assignment': assignment,
        'form': form
    }

    # Render the template with the provided context
    return render(request, 'academic/assignment_grading.html', context)


def teacher_exams(request):
    if request.method == 'POST':
        form = GradeInsertionForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']
            url = reverse('academic:teacher_exams_list_exams', kwargs={
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

    return render(request, 'academic/teacher_exams.html', {'form': form})


def teacher_exams_list_students(request, year_id, class_id, section_id, subject_id):
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)
    subject = Subject.objects.get(subjectID=subject_id)

    students = Student.objects.filter(
        currentYear=year.yearID,
        currentClass=clas.classID,
        currentSection=section.sectionID,
        studentsubject__subjectID=subject.subjectID
    )

    context = {
        'year': year,
        'class': clas,
        'section': section,
        'subject': subject,
        'students': students
    }

    # Render the template with the provided context
    return render(request, 'academic/teacher_exams_list_students.html', context)


def teacher_exams_new_exam(request, year_id, class_id, section_id, subject_id):
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)
    subject = Subject.objects.get(subjectID=subject_id)

    students = Student.objects.filter(
        currentYear=year.yearID,
        currentClass=clas.classID,
        currentSection=section.sectionID,
        studentsubject__subjectID=subject.subjectID
    )

    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)  # Don't save yet, to set ForeignKey fields manually

            for student in students:
                # Create a new Assignment object for each student
                exam = Exam(
                    year=year,
                    school_class=clas,
                    section=section,
                    student=student,
                    subject=subject,
                    teacher=UserEmployee.objects.get(username=request.user.username).employee,
                    title=exam.title,
                    date=exam.date,
                    description=exam.description
                )
                exam.save()  # Save the new assignment record
            return redirect('academic:teacher_exams_list_exams', year_id=year_id, class_id=class_id,
                            section_id=section_id, subject_id=subject_id)
    else:
        form = ExamForm()

    context = {
        'year': year,
        'class': clas,
        'section': section,
        'subject': subject,
        'form': form
    }

    # Render the template with the provided context
    return render(request, 'academic/teacher_exams_new_exam.html', context)


def exams_for_student(request, student_id, year_id, class_id, section_id, subject_id):
    student = get_object_or_404(Student, pk=student_id)
    year = StudyYear.objects.get(yearID=year_id)
    clas = Class.objects.get(classID=class_id)
    section = Section.objects.get(sectionID=section_id)
    subject = Subject.objects.get(subjectID=subject_id)

    exams = Exam.objects.filter(
        year=year,
        school_class=clas,
        section=section,
        subject=subject,
        student=student,
        teacher=UserEmployee.objects.get(username=request.user.username).employee
    ).order_by("-date")

    context = {
        'student': student,
        'year': year,
        'class': clas,
        'section': section,
        'subject': subject,
        'exams': exams
    }

    # Render the template with the provided context
    return render(request, 'academic/exams_for_student.html', context)


def exam_grading(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)

    if request.method == 'POST':
        form = ExamGradeUpdateForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
    else:
        form = ExamGradeUpdateForm(instance=exam)

    context = {
        'exam': exam,
        'form': form
    }

    # Render the template with the provided context
    return render(request, 'academic/exam_grading.html', context)


def admin_record_attendenceI(request):
    if request.method == 'POST':
        form = AttendenceForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']

            url = reverse('academic:admin_record_attendenceII',
                          kwargs={'year_id': year.yearID, 'class_id': school_class.classID,
                                  'section_id': section.sectionID})
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = AttendenceForm()

    return render(request, 'academic/admin_record_attendenceI.html', {'form': form})


def admin_record_attendenceII(request, year_id, class_id, section_id):
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

    return render(request, 'academic/admin_record_attendenceII.html', context)


def admin_record_attendenceIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = AttendanceRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)  # Don't save yet, to set ForeignKey fields manually
            record = Attendance(
                year=student.currentYear,
                school_class=student.currentClass,
                section=student.currentSection,
                student=student,
                date=record.date,
                reason=record.reason,
                excuse=record.excuse,
                notes=record.notes,
                insertedUserID=UserEmployee.objects.get(username=request.user.username).employee,
                insertingTime=datetime.now()
            )
            record.save()
            return redirect('academic:admin_record_attendenceIIII', student.studentID)
    else:
        form = AttendanceRecordForm()

    context = {
        'student': student,
        'form': form
    }
    return render(request, 'academic/admin_record_attendenceIII.html', context)


def admin_record_attendenceIIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    records = Attendance.objects.filter(
        student=student
    ).order_by('-date')

    context = {
        'student': student,
        'records': records
    }
    return render(request, 'academic/admin_record_attendenceIIII.html', context)


def admin_record_attendence_edit(request, attendence_id):
    attendence = get_object_or_404(Attendance, pk=attendence_id)

    if request.method == 'POST':
        form = AttendanceRecordForm(request.POST, instance=attendence)
        if form.is_valid():
            form.save()
            url = reverse('academic:admin_record_attendenceIIII',
                          kwargs={'student_id': attendence.student.studentID})
            return redirect(url)
    else:
        form = AttendanceRecordForm(instance=attendence)  # Prepopulate the form with existing data

    return render(request, 'academic/admin_record_attendence_edit.html', {'form': form})


def secretary_record_attendenceI(request):
    if request.method == 'POST':
        form = AttendenceForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']

            url = reverse('academic:secretary_record_attendenceII',
                          kwargs={'year_id': year.yearID, 'class_id': school_class.classID,
                                  'section_id': section.sectionID})
            return redirect(url)


        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = AttendenceForm()

    return render(request, 'academic/secretary_record_attendenceI.html', {'form': form})


def secretary_record_attendenceII(request, year_id, class_id, section_id):
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

    return render(request, 'academic/secretary_record_attendenceII.html', context)


def secretary_record_attendenceIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = AttendanceRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)  # Don't save yet, to set ForeignKey fields manually
            record = Attendance(
                year=student.currentYear,
                school_class=student.currentClass,
                section=student.currentSection,
                student=student,
                date=record.date,
                reason=record.reason,
                excuse=record.excuse,
                notes=record.notes,
                insertedUserID=UserEmployee.objects.get(username=request.user.username).employee,
                insertingTime=datetime.now()
            )
            record.save()
            return redirect('academic:secretary_record_attendenceIIII', student.studentID)
    else:
        form = AttendanceRecordForm()

    context = {
        'student': student,
        'form': form
    }
    return render(request, 'academic/secretary_record_attendenceIII.html', context)


def secretary_record_attendenceIIII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    records = Attendance.objects.filter(
        student=student
    ).order_by('-date')

    context = {
        'student': student,
        'records': records
    }
    return render(request, 'academic/secretary_record_attendenceIIII.html', context)


def secretary_record_attendence_edit(request, attendence_id):
    attendence = get_object_or_404(Attendance, pk=attendence_id)

    if request.method == 'POST':
        form = AttendanceRecordForm(request.POST, instance=attendence)
        if form.is_valid():
            form.save()
            url = reverse('academic:secretary_record_attendenceIIII',
                          kwargs={'student_id': attendence.student.studentID})
            return redirect(url)
    else:
        form = AttendanceRecordForm(instance=attendence)  # Prepopulate the form with existing data

    return render(request, 'academic/secretary_record_attendence_edit.html', {'form': form})


def teacher_insert_grades2(request):
    if request.method == 'POST':
        form = GradeInsertionForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            year = form.cleaned_data['year']
            school_class = form.cleaned_data['school_class']
            section = form.cleaned_data['section']

            # Fetch all students matching the selected criteria
            students = Student.objects.filter(
                currentYear=year.yearID,
                currentClass=school_class.classID,
                currentSection=section.sectionID,
                studentsubject__subjectID=subject.subjectID
            )

            # Pass students and grades to the template
            student_grades = []
            for student in students:
                # Try to get the grade record for the student
                try:
                    grade = Grade.objects.get(
                        student=student,
                        year=year,
                        school_class=school_class,
                        section=section,
                        subject=subject
                    )
                except Grade.DoesNotExist:
                    grade = None

                student_grades.append((student, grade))

            return render(request, 'academic/insert_grades.html', {
                'student_grades': student_grades,
                'subject': subject,
                'year': year,
                'class': school_class,
                'section': section
            })
    else:
        form = GradeInsertionForm()

    return render(request, 'academic/teacher_insert_grades2.html', {'form': form})


def save_grades(request):
    if request.method == 'POST':
        # Retrieve data from POST request
        subject_id = request.POST.get('subject_id')
        year_id = request.POST.get('year_id')
        class_id = request.POST.get('class_id')
        section_id = request.POST.get('section_id')

        # Fetch all students matching the selected criteria
        students = Student.objects.filter(
            currentYear=year_id,
            currentClass=class_id,
            currentSection=section_id,
            studentsubject__subjectID=subject_id
        )

        # Process grades for each student
        for student in students:
            # Retrieve grade data from POST request
            first_quarter = request.POST.get(f'first_quarter_{student.studentID}')
            second_quarter = request.POST.get(f'second_quarter_{student.studentID}')
            third_quarter = request.POST.get(f'third_quarter_{student.studentID}')
            fourth_quarter = request.POST.get(f'fourth_quarter_{student.studentID}')

            # Convert empty strings to None
            first_quarter = float(first_quarter) if first_quarter else None
            second_quarter = float(second_quarter) if second_quarter else None
            third_quarter = float(third_quarter) if third_quarter else None
            fourth_quarter = float(fourth_quarter) if fourth_quarter else None

            # Check if a grade record already exists for the student
            grade_record = Grade.objects.filter(
                student=student,
                year_id=year_id,
                school_class_id=class_id,
                section_id=section_id,
                subject_id=subject_id
            ).first()

            # If a record exists, update it; otherwise, create a new record
            if grade_record:
                grade_record.firstQuarter = first_quarter
                grade_record.secondQuarter = second_quarter
                grade_record.thirdQuarter = third_quarter
                grade_record.fourthQuarter = fourth_quarter
                grade_record.save()
            else:
                Grade.objects.create(
                    student=student,
                    year_id=year_id,
                    school_class_id=class_id,
                    section_id=section_id,
                    subject_id=subject_id,
                    firstQuarter=first_quarter,
                    secondQuarter=second_quarter,
                    thirdQuarter=third_quarter,
                    fourthQuarter=fourth_quarter,
                    teacher=UserEmployee.objects.get(username=request.user.username).employee
                )

        # Redirect or render success message
        return redirect('academic:teacher_insert_grades2')

    # Redirect to teacher_insert_grades view if request method is not POST
    return redirect('academic:teacher_insert_grades2')


def admin_new_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ClassForm()
    return render(request, 'academic/admin_new_class.html', {'form': form})


def admin_new_section(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SectionForm()
    return render(request, 'academic/admin_new_section.html', {'form': form})


def admin_new_subject(request):
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST)
        class_subject_form = ClassSubjectForm(request.POST)

        if subject_form.is_valid() and class_subject_form.is_valid():
            # Save the Subject instance
            subject = subject_form.save()

            # Create and save the ClassSubject instance
            class_subject = ClassSubject(
                school_class=class_subject_form.cleaned_data['school_class'],
                subject=subject,
                year=class_subject_form.cleaned_data['year'],
                teacher=class_subject_form.cleaned_data['teacher']
            )
            class_subject.save()

            students = Student.objects.filter(
                currentClass=class_subject.school_class,
                currentYear=class_subject.year
            )

            if students:
                for student in students:
                    StudentSubject.objects.create(
                        studentID=student,
                        subjectID=subject
                    )


    else:
        subject_form = SubjectForm()
        class_subject_form = ClassSubjectForm()

    return render(request, 'academic/admin_new_subject.html', {
        'subject_form': subject_form,
        'class_subject_form': class_subject_form
    })


def secretary_new_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ClassForm()
    return render(request, 'academic/secretary_new_class.html', {'form': form})


def secretary_new_section(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SectionForm()
    return render(request, 'academic/secretary_new_section.html', {'form': form})


def secretary_new_subject(request):
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST)
        class_subject_form = ClassSubjectForm(request.POST)

        if subject_form.is_valid() and class_subject_form.is_valid():
            # Save the Subject instance
            subject = subject_form.save()

            # Create and save the ClassSubject instance
            class_subject = ClassSubject(
                school_class=class_subject_form.cleaned_data['school_class'],
                subject=subject,
                year=class_subject_form.cleaned_data['year'],
                teacher=class_subject_form.cleaned_data['teacher']
            )
            class_subject.save()

            students = Student.objects.filter(
                currentClass=class_subject.school_class,
                currentYear=class_subject.year
            )

            if students:
                for student in students:
                    StudentSubject.objects.create(
                        studentID=student,
                        subjectID=subject
                    )


    else:
        subject_form = SubjectForm()
        class_subject_form = ClassSubjectForm()

    return render(request, 'academic/secretary_new_subject.html', {
        'subject_form': subject_form,
        'class_subject_form': class_subject_form
    })


def admin_new_year(request):
    if request.method == 'POST':
        study_year_form = StudyYearForm(request.POST)
        school_sittings_form = SchoolSittingsForm(request.POST)

        if study_year_form.is_valid() and school_sittings_form.is_valid():
            # Save the StudyYear instance
            study_year = study_year_form.save()

            # Create and save the SchoolSittings instance
            school_sittings = SchoolSittings(
                year=study_year,
                startDate=school_sittings_form.cleaned_data['startDate'],
                endDate=school_sittings_form.cleaned_data['endDate']
            )
            school_sittings.save()


    else:
        study_year_form = StudyYearForm()
        school_sittings_form = SchoolSittingsForm()

    return render(request, 'academic/admin_new_year.html', {
        'study_year_form': study_year_form,
        'school_sittings_form': school_sittings_form
    })


def admin_edit_studentI(request):
    if request.method == 'POST':
        form = StudentSelection(request.POST)
        if form.is_valid():
            # Save the attendance record
            student = form.cleaned_data['student']
            return redirect('academic:admin_edit_studentII', student_id=student.pk)  # Redirect to a relevant page
        else:
            messages.error(request, 'There was an error recording the attendance. Please try again.')
    else:
        form = StudentSelection()

    return render(request, 'academic/admin_edit_studentI.html', {'form': form})

def admin_edit_studentII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('academic:admin_edit_studentII', student_id=student_id)  # Change to your desired redirect URL

        else:
            messages.error(request, 'There was an error updating the student details. Please try again.')
    else:
        form = StudentForm(instance=student)

    return render(request, 'academic/admin_edit_studentII.html', {'form': form, 'student': student})


def secretaty_edit_studentI(request):
    if request.method == 'POST':
        form = StudentSelection(request.POST)
        if form.is_valid():
            # Save the attendance record
            student = form.cleaned_data['student']
            return redirect('academic:secretaty_edit_studentII', student_id=student.pk)  # Redirect to a relevant page
        else:
            messages.error(request, 'There was an error recording the attendance. Please try again.')
    else:
        form = StudentSelection()

    return render(request, 'academic/secretaty_edit_studentI.html', {'form': form})

def secretaty_edit_studentII(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('academic:secretaty_edit_studentII', student_id=student_id)  # Change to your desired redirect URL

        else:
            messages.error(request, 'There was an error updating the student details. Please try again.')
    else:
        form = StudentForm(instance=student)

    return render(request, 'academic/secretaty_edit_studentII.html', {'form': form, 'student': student})

def admin_edit_employeeI(request):
    if request.method == 'POST':
        form = EmployeeSelectionForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            return redirect('academic:admin_edit_employeeII', employee_id=employee.pk)
        else:
            messages.error(request, 'There was an error selecting the employee. Please try again.')
    else:
        form = EmployeeSelectionForm()

    return render(request, 'academic/admin_edit_employeeI.html', {'form': form})


def admin_edit_employeeII(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('academic:admin_edit_employeeII', employee_id=employee_id)  # Redirect to the same page or another relevant page
        else:
            messages.error(request, 'There was an error updating the employee details. Please try again.')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'academic/admin_edit_employeeII.html', {'form': form, 'employee': employee})

