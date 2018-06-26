from django import forms
from django.forms import ModelForm
from .models import Project, ProjectElement, Folder, Account

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
    account = forms.CharField(max_length = 30, required = False)
    accounts = forms.CharField(required = False)
    class Meta:
        model = Project
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['accounts'].widget = forms.HiddenInput()

class ElementForm(ModelForm):
    class Meta:
        model = ProjectElement
        fields = ['name', 'description', 'parent']

    def __init__(self, current_project_id, *args, **kwargs):
        super(ElementForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Folder.objects.filter(project = current_project_id)

class FolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent']

    def __init__(self, current_project_id, *args, **kwargs):
        super(FolderForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Folder.objects.filter(project = current_project_id)
