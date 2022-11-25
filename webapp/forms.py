from django import forms
from django.forms import widgets, ValidationError
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

    def clean_summary(self):
        summary = self.cleaned_data['summary']
        if len(summary) < 5:
            # raise ValidationError('Краткое описание должно быть не менее %(length)d символов!', code='too_short', params={'length': 5})
            self.add_error('summary', ValidationError('Краткое описание должно быть не менее %(length)d символов!', code='too_short', params={'length': 5}))
        return summary
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['summary'] == cleaned_data['description']:
            raise ValidationError('Текст краткого и полного описания не должны дублировать друг друга')
    
    # def clean_description(self):
    #     description = self.cleaned_data['description']
    #     if len(description) < 10:
    #         raise ValidationError('Полное описание слишком короткое! Должно быть не менее %(length)d символов!', code='too_short', params={'length': 10})
    #     return description
