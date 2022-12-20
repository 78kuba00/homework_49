from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']



# class MyUserCreationForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     email = forms.EmailField(max_length=100, required=True)
#     password = forms.CharField(label="Пароль", strip=False, required=True, widget=forms.PasswordInput)
#     password_confirm = forms.CharField(label="Подтвердите пароль", required=True, widget=forms.PasswordInput, strip=False)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirm = cleaned_data.get("password_confirm")
#         if password and password_confirm and password != password_confirm:
#             raise forms.ValidationError('Пароли не совпадают!')
#         return cleaned_data
#
#     # def clean_first_name(self):
#     #     first_name = self.cleaned_data['first_name']
#     #     name_empty = []
#     #     if name_empty:
#     #         raise forms.ValidationError('Надо в ОБЯЗ набрать имя')
#
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     user.first_name = '{}'.format(
    #         self.cleaned_data['first_name'],
    #     )
    #     if commit:
    #         user.save()
    #     return user
#
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']