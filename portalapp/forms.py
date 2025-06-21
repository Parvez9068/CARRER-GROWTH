from portalapp.models import Job
from django.forms import ModelForm


class RegisterJob(ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
        

from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'resume']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name should not contain numbers.")
        return name


