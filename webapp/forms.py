from django import forms
from django.forms import widgets, ValidationError
from webapp.models import Tracker, TrackerType, TrackerStatus


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = ['summary', 'description', 'status', 'type']
        widgets = {
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': widgets.CheckboxSelectMultiple,
            'type': widgets.CheckboxSelectMultiple
        }
        error_messages = {
            'description': {
                'required': 'Поле должно быть заполнено'
            }
        }

    def clean_summary(self):
        summary = self.cleaned_data['summary']
        if len(summary) < 5:
            # raise ValidationError('Краткое описание должно быть не менее %(length)d символов!', code='too_short', params={'length': 5})
            self.add_error('summary', ValidationError('Краткое описание должно быть не менее %(length)d символов!', code='too_short', params={'length': 5}))
        return summary

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 10:
            self.add_error('description', ValidationError('Полное описание слишком короткое! Должно быть не менее %(length)d символов!', code='too_short', params={'length': 10}))
        return description

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['summary'] == cleaned_data.get('description', ''):
            raise ValidationError('Текст краткого и полного описания не должны дублировать друг друга')
    

