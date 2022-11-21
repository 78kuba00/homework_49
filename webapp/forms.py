from django import forms
from django.forms import widgets
from webapp.models import Tracker, TrackerType, TrackerStatus

class TaskForm(forms.Form):
    summary = forms.CharField(max_length=200, required=True, label='Краткое описание')
    description = forms.CharField(max_length=3000, required=False, label='Полное описание', widget=widgets.Textarea)
    status = forms.ModelChoiceField(queryset=TrackerStatus.objects.all(), required=True, label='Статус')
    type = forms.ModelChoiceField(queryset=TrackerType.objects.all(), required=True, label='Тип')

# class SearchForm(forms.Form):
#     search = forms.CharField(max_length=50, required=False, label="Найти")