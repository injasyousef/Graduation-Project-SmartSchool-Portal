from django import forms
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User

from users.models import UserStudent, Employee, UserEmployee, Student
from django.core.exceptions import ValidationError

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomPasswordChangeForm(PasswordChangeForm):
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("This email address is not associated with any account.")
        return email

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'employmentDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'exitDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UserEmployeeForm(forms.ModelForm):
    class Meta:
        model = UserEmployee
        fields = ['year','username', 'password', 'isActive']
        widgets = {
            'password': forms.PasswordInput(),  # Render the password field as a password input
        }

    def __init__(self, *args, **kwargs):
        super(UserEmployeeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserEmployee.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'birthDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UserStudentForm(forms.ModelForm):
    class Meta:
        model = UserStudent
        fields = ['year', 'username', 'password', 'parentUsername','parentPassword','isActive','Financialactive']
        widgets = {
            'password': forms.PasswordInput(),  # Render the password field as a password input
            'parentPassword': forms.PasswordInput(),  # Render the password field as a password input

        }

    def __init__(self, *args, **kwargs):
        super(UserStudentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserStudent.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_parentUsername(self):
        parentUsername = self.cleaned_data.get('parentUsername')
        if UserStudent.objects.filter(parentUsername=parentUsername).exists():
            raise forms.ValidationError("This parent username is already taken.")
        return parentUsername



