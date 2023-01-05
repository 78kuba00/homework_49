from django import forms
from django.contrib.auth import get_user_model
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
        fields = ['title', 'description', 'start_at', 'end_at']

class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')

class ChangeUsersInProjectsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.users = kwargs.pop('users')
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = get_user_model().objects.exclude(pk=self.users.pk)
    class Meta:
        model = Project
        fields = ['users']
        widgets = {'users': widgets.CheckboxSelectMultiple}

    def save(self, commit=True):
        project = super().save(commit=commit)
        if commit:
            project.users.add(self.users)
            project.save()
        return project


class TaskWithProjectForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = ['summary', 'status', 'type', 'description']
        widgets = {
            'summary': widgets.TextInput(attrs={'class': 'form-control mb-3',
                                              'placeholder': 'Название задачи'}),
            'status': widgets.Select(attrs={'class': 'form-control mb-3'}),
            'type': widgets.CheckboxSelectMultiple,
            'description': widgets.Textarea(attrs={'class': 'form-control mb-3', 'rows': 6,
                                               'placeholder': 'Основной Текст'})
        }

    regular_int = "\\d"
    html_tags_regular = r'([<>].+?[</>])'