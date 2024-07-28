# academic/forms.py
from django import forms
from django.forms import ClearableFileInput
from django.http import request

from academic.models import StudyYear, Subject, Assignment, ClassSubject, Section, Class, Grade, Exam, Attendance, \
    SchoolSittings
from finance.models import Payments, StudentFees
from users.models import UserEmployee, Student, Employee


class YearFilterForm(forms.Form):
    year = forms.ModelChoiceField(queryset=StudyYear.objects.all(), required=False)


class GradeInsertionForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['year', 'school_class', 'section', 'subject']
        widgets = {
            'year': forms.Select(attrs={'class': 'form-control'}),
            'school_class': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        last_year = StudyYear.objects.last()
        if last_year:
            self.fields['year'].initial = last_year.yearID

        self.fields['year'].queryset = StudyYear.objects.filter(pk=last_year.pk)

        year_id = self.data.get('year') if self.is_bound else self.initial.get('year')
        class_id = self.data.get('school_class') if self.is_bound else self.initial.get('school_class')

        self.fields['school_class'].queryset = Class.objects.all()

        if year_id:
            self.fields['school_class'].queryset = Class.objects.filter(
                classsubject__year_id=year_id
            ).distinct()

        if year_id and class_id:
            self.fields['section'].queryset = Section.objects.filter(
                school_class_id=class_id
            ).order_by('sectionSymbol')

            self.fields['subject'].queryset = Subject.objects.filter(
                classsubject__school_class_id=class_id,
                classsubject__year_id=year_id
            ).distinct()
        else:
            self.fields['section'].queryset = Section.objects.none()
            self.fields['subject'].queryset = Subject.objects.none()

        self.fields['year'].widget = forms.HiddenInput()



class NewAssForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['year', 'school_class','subject']
        widgets = {
            'year': forms.Select(attrs={'class': 'form-control'}),
            'school_class': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        year_id = self.data.get('year') if self.is_bound else None
        class_id = self.data.get('school_class') if self.is_bound else None

        self.fields['school_class'].queryset = Class.objects.all()  # Assuming you want to list all classes

        if year_id and class_id:
            # Adjusting the subject queryset based on selected class and year
            # This assumes that subjects are linked to classes and years through the ClassSubject model
            self.fields['subject'].queryset = Subject.objects.filter(
                classsubject__school_class_id=class_id,
                classsubject__year_id=year_id
            ).distinct()
        else:
            self.fields['subject'].queryset = Subject.objects.none()


class SubjectFilterForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False)



class AttendanceYearFilterForm(forms.Form):
    year = forms.ModelChoiceField(queryset=StudyYear.objects.all(), required=False)

from django import forms

class UnclickableFileSubmitWidget(forms.ClearableFileInput):
    template_name = 'academic/unclickable_file_submit_widget.html'  # Path to the custom template

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['submit_text', 'fileSubmit', 'link']
        widgets = {
            'submit_text': forms.Textarea(attrs={'rows': 10,'columns':1}),
            'fileSubmit': UnclickableFileSubmitWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(AssignmentSubmissionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class AssignmentForm(forms.ModelForm):
    dueDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'dueDate','linkInsert','fileInsert']


class AssignmentGradeUpdateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assignmentGrade', 'assignmentFinalGrade']

class ExamForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Exam
        fields = ['title', 'description', 'date']

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ExamGradeUpdateForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['examGrade', 'finalGrade']

class AttendenceForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['year', 'school_class', 'section']
        widgets = {
            'year': forms.Select(attrs={'class': 'form-control'}),
            'school_class': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school_class'].queryset = Class.objects.all()

        # Set initial value for the year field to the last year object
        last_year = StudyYear.objects.last()
        if last_year:
            self.fields['year'].initial = last_year.pk

        class_id = self.data.get('school_class') if self.is_bound else None
        if class_id:
            self.fields['section'].queryset = Section.objects.filter(school_class_id=class_id).order_by('sectionSymbol')
        else:
            self.fields['section'].queryset = Section.objects.none()

        self.fields['year'].widget = forms.HiddenInput()


class AttendanceRecordForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Attendance
        fields = ['date', 'reason', 'excuse', 'notes']

    def __init__(self, *args, **kwargs):
        super(AttendanceRecordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = ['amount', 'date', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class StudentFeesForm(forms.ModelForm):
    class Meta:
        model = StudentFees
        fields = ['exemptions', 'exemptionsDetail']
        widgets = {
            'exemptions': forms.NumberInput(attrs={'class': 'form-control'}),
            'exemptionsDetail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['className', 'classNameOther','next_class', 'isActive']

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['year', 'school_class', 'sectionSymbol', 'description', 'supervisor']

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'subjectTextBook']

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ClassSubjectForm(forms.Form):
    school_class = forms.ModelChoiceField(queryset=Class.objects.all())
    teacher = forms.ModelChoiceField(queryset=Employee.objects.all())
    year = forms.ModelChoiceField(queryset=StudyYear.objects.all())

    def __init__(self, *args, **kwargs):
        super(ClassSubjectForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class StudyYearForm(forms.ModelForm):
    class Meta:
        model = StudyYear
        fields = ['yearName']

    def __init__(self, *args, **kwargs):
        super(StudyYearForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class SchoolSittingsForm(forms.ModelForm):
    class Meta:
        model = SchoolSittings
        fields = ['startDate', 'endDate']
        widgets = {
            'startDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'endDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SchoolSittingsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class StudentSelection(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['year', 'school_class', 'section', 'student']
        widgets = {
            'year': forms.Select(attrs={'class': 'form-control'}),
            'school_class': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school_class'].queryset = Class.objects.all()
        self.fields['student'].queryset = Student.objects.none()

        last_year = StudyYear.objects.last()
        if last_year:
            self.fields['year'].initial = last_year.pk

        class_id = self.data.get('school_class') if self.is_bound else None
        section_id = self.data.get('section') if self.is_bound else None
        if class_id and section_id:
            self.fields['section'].queryset = Section.objects.filter(school_class_id=class_id).order_by('sectionSymbol')
            self.fields['student'].queryset = Student.objects.filter(currentClass_id=class_id, currentSection_id=section_id)
        else:
            self.fields['section'].queryset = Section.objects.none()
            self.fields['student'].queryset = Student.objects.none()
        self.fields['year'].widget = forms.HiddenInput()


class EmployeeSelectionForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))