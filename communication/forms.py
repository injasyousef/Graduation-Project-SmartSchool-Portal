# communication/forms.py

from django import forms

from academic.models import ClassSubject, Lecture, StudentSubject
from communication.models import Message, Advertisement
from users.models import UserEmployee, UserStudent, Student, Employee


class SendMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_student = kwargs.pop('user_student', None)
        super(SendMessageForm, self).__init__(*args, **kwargs)

        if user_student:
            student_instance = user_student.student

            # Get subjects for the student
            student_subjects = StudentSubject.objects.filter(studentID=student_instance)
            subject_ids = student_subjects.values_list('subjectID', flat=True)

            # Get teachers for the student
            teachers_for_student = Employee.objects.filter(classsubject__subject__in=subject_ids)

            # Get employees with role 'secretary' or 'admin'
            secretaries_and_admins = Employee.objects.filter(rule__in=['secretary', 'admin'])

            # Combine the teachers and the secretaries/admins
            all_relevant_employees = teachers_for_student | secretaries_and_admins
            all_relevant_employees = all_relevant_employees.distinct()

            # Prepare the choices for the receiverEmployee field
            teacher_choices = [(teacher.employeeID, teacher.fullName) for teacher in all_relevant_employees]

            self.fields['receiverEmployee'].choices = teacher_choices

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Message
        fields = ['title', 'content', 'file', 'receiverEmployee']
        widgets = {
            'receiverEmployee': forms.Select(attrs={'class': 'form-control'}),
        }

class TeacherMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content', 'file']

    def __init__(self, *args, **kwargs):
        super(TeacherMessageForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

