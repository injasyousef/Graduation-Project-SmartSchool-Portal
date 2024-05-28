from academic import forms
# from finance.models import Payments, StudentFees
#
#
# class PaymentsForm(forms.ModelForm):
#     class Meta:
#         model = Payments
#         fields = ['amount', 'date', 'description']
#         widgets = {
#             'amount': forms.NumberInput(attrs={'class': 'form-control'}),
#             'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }
#
# class StudentFeesForm(forms.ModelForm):
#     class Meta:
#         model = StudentFees
#         fields = ['exemptions', 'exemptionsDetail']
#         widgets = {
#             'exemptions': forms.NumberInput(attrs={'class': 'form-control'}),
#             'exemptionsDetail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }