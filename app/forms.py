from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=5, widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length=8, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password_check != password:
            raise ValidationError("Passwords do not match")

    def save(self,**kwargs):
        self.cleaned_data.pop('password_check')
        return User.objects.create_user(**self.cleaned_data)