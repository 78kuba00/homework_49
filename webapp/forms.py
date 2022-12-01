from django import forms
from django.forms import widgets
from webapp.models import Tracker, TrackerType, TrackerStatus

# class TaskForm(forms.Form):
#     summary = forms.CharField(max_length=200, required=True, label='Краткое описание')
#     description = forms.CharField(max_length=3000, required=True, label='Полное описание', widget=widgets.Textarea)
#     status = forms.ModelChoiceField(queryset=TrackerStatus.objects.all(), required=True, label='Статус')
#     type = forms.ModelMultipleChoiceField(queryset=TrackerType.objects.all(), required=True, label='Тип')

# class SearchForm(forms.Form):
#     search = forms.CharField(max_length=50, required=False, label="Найти")

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = ['summary', 'description', 'status', 'type']
        widgets = {'status': widgets.CheckboxInput, 'type': widgets.CheckboxSelectMultiple}
        # type = {'type': widgets.CheckboxSelectMultiple}

class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')