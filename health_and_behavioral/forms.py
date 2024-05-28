
from django import forms

from academic.models import StudyYear
from health_and_behavioral.models import BehaviourEvaluation, HealthRecord


class YearFilterForm(forms.Form):
    year = forms.ModelChoiceField(queryset=StudyYear.objects.all(), required=False)

class BehavioralRecord(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = BehaviourEvaluation
        fields = ['date', 'description', 'action', 'notes']

    def __init__(self, *args, **kwargs):
        super(BehavioralRecord, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
class HealthRecordForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = HealthRecord
        fields = ['diagnosis', 'action', 'date', 'description', 'parentsHaveBeenContacted']

    def __init__(self, *args, **kwargs):
        super(HealthRecordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
