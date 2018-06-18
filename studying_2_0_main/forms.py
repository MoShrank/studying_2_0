from django import forms
from django.forms import ModelForm
from .models import Project, ProjectElement

class AccountForm(forms.Form):
        username = forms.CharField(max_length = 30)
        password = forms.CharField(widget=forms.PasswordInput, max_length = 30)
        email_address = forms.CharField(max_length = 30)
        widgets = {'username' : forms.TextInput(attrs={'class' : 'register'}),
                    'password': forms.PasswordInput(attrs={'class': 'register'}),
                    'email_address' : forms.TextInput(attrs={'class' : 'register'})
                    }

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 30)
    password = forms.CharField(widget=forms.PasswordInput, max_length = 30)

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'accounts']

class ElementForm(ModelForm):
    class Meta:
        model = ProjectElement
        fields = ['name', 'description']