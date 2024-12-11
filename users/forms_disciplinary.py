from django import forms
from .models import DisciplinaryIncident, Sanction, Student

class IncidentForm(forms.ModelForm):
    class Meta:
        model = DisciplinaryIncident
        fields = ['student', 'description', 'severity_level']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class SanctionForm(forms.ModelForm):
    class Meta:
        model = Sanction
        fields = ['description', 'duration']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'duration': forms.NumberInput(attrs={'min': 1, 'max': 30}),
        }

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        severity_level = self.instance.severity_level.level_description if self.instance else None

        if severity_level == 'MINOR' and (duration < 1 or duration > 2):
            raise forms.ValidationError('Minor sanctions must have duration between 1-2 days')
        elif severity_level == 'MODERATE' and (duration < 3 or duration > 5):
            raise forms.ValidationError('Moderate sanctions must have duration between 3-5 days')
        elif severity_level == 'SEVERE' and duration < 7:
            raise forms.ValidationError('Severe sanctions must have duration of at least 7 days')

        return duration

class StudentSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by name or ID...'})
    )
    grade_level = forms.ChoiceField(
        choices=[('', 'All Grades')] + [(i, f'Grade {i}') for i in range(7, 13)],
        required=False
    )
    section = forms.CharField(required=False)

    def search_students(self):
        search = self.cleaned_data.get('search', '')
        grade_level = self.cleaned_data.get('grade_level', '')
        section = self.cleaned_data.get('section', '')

        students = Student.objects.all()

        if search:
            students = students.filter(
                models.Q(name__icontains=search) |
                models.Q(student_id__icontains=search)
            )

        if grade_level:
            students = students.filter(grade_level=grade_level)

        if section:
            students = students.filter(section__icontains=section)

        return students
