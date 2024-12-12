from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import DisciplinaryIncident, Profile

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class IncidentForm(forms.ModelForm):
    class Meta:
        model = DisciplinaryIncident
        fields = ("student", "description","date","severity_level","sanction","reported_by")
        widgets = {
            'student' : forms.TextInput(attrs = {'class': 'form-control my-5'}),
            'description' : forms.TextInput(attrs = {'class': 'form-control my-5'}),
            'date' : forms.DateTimeInput(),
            'severity_level' : forms.Select(attrs = {'class': 'form-control my-5'}),
            'sanction' : forms.Select(attrs = {'class': 'form-control my-5'}),
            'reported_by' : forms.TextInput(attrs = {'class': 'form-control my-5'}),
        }

        labels = {
            'student' : "Enter student name:",
            'description' : "Enter description:",
            'data' : "Enter date:",
            'severity_level' : "Severity Level:",
            'sanction' : "Sanction:",
            'reported_by' : "Reported by:",
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("user", "bio")
        widgets = {
            'user' : forms.Select(attrs = {'class': 'form-control my-5'}),
            'bio' : forms.TextInput(attrs = {'class': 'form-control my-5'}),
        }

        labels = {
            'user' : "Select User:",
            'bio' : "Enter Bio:",
        }

