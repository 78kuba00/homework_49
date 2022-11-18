from django import forms
from django.forms import widgets
from webapp.models import Tracker, TrackerType, TrackerStatus

class TaskForm(forms.Form):
    summary = forms.CharField(max_length=200, required=False, label='Краткое описание')
    description = forms.CharField(max_length=3000, required=True, label='Полное описание', widget=widgets.Textarea)
    status = forms.ChoiceField(choices=TrackerStatus, label='Статус')
    type = forms.ChoiceField(choices=TrackerType, label='Тип')

# class SearchForm(forms.Form):
#     search = forms.CharField(max_length=50, required=False, label="Найти")