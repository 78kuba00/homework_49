from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Tracker, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = ['summary', 'description', 'status', 'type']
        widgets = {'status': widgets.Select, 'type': widgets.CheckboxSelectMultiple}
        # type = {'type': widgets.CheckboxSelectMultiple}

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = []

class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')