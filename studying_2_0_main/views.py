from django.shortcuts import render, redirect
from django.template import loader
from .forms import AccountForm, LoginForm, ProjectForm, ElementForm, FolderForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from .models import Project, ProjectElement, Folder, Tag
from datetime import date
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from .decorators import user_is_project_author
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import resolve


project_decorator = [login_required, user_is_project_author]


    #views that require a login:


    #views for project:

@method_decorator(login_required, name='dispatch')
class Projects(ListView):
    context_object_name = 'project_list'
    template_name = 'projects.html'

    def get_queryset(self):
        return Project.objects.filter(accounts__username=self.request.user)

@method_decorator(login_required, name='dispatch')
class NewProject(CreateView):
    form_class = ProjectForm
    template_name = 'new_project.html'
    success_url = '/projects/'

    def form_valid(self, form):
        form.save()
        form.instance.accounts.add(self.request.user)
        account_list = self.request.POST.getlist('accounts')
        for account in account_list:
            form.instance.accounts.add(User.objects.get(username=account))
        form.instance.save()

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EditProject(UpdateView):
    form_class = ProjectForm
    template_name = 'edit_project.html'
    success_url = '/projects/'

    def delete_element(self):
        try:
            for folder in self.request.POST.getlist('folder'):

                folder_obj = Folder.objects.get(id=folder)

                folder_childs = Folder.objects.filter(parent=folder_obj.pk) #sets all folders inside folder_obj to folder_obj parent
                if folder_childs:
                    folder_obj.set_parents(folder_childs)

                folder_childs = ProjectElement.objects.filter(parent=folder_obj.pk) #sets all elements inside folder_obj to folder_obj parent
                if folder_childs:
                    folder_obj.set_parents(folder_childs)

                folder_obj.delete()

        except Exception:
            print('no folder to delete')

        try:
            for element in self.request.POST.getlist('element'):
                ProjectElement.objects.get(id=element).delete()
        except Exception:
            print("no element to delete")

    def get_object(self, queryset=None):
        return Project.objects.get(id=self.kwargs["project_id"])

    def form_valid(self, form):
        new_account_list = self.request.POST.getlist('accounts')
        obj = self.get_object()
        if 'delete' in self.request.POST:
            self.delete_element()
            self.success_url = self.success_url + str(obj.id) + '/edit'


        elif 'edit' in self.request.POST:
            self.success_url = self.success_url + str(obj.id) + '/edit/'
            if not self.request.POST.get('folder'):
                self.success_url = self.success_url + 'element/' + self.request.POST.get('element')
            else:
                folder_id = self.request.POST.get('folder')
                self.success_url = self.success_url + 'folder/' + folder_id

        else:
            self.success_url = self.success_url + obj.slug + '-' + str(obj.id)

        obj.accounts.clear()
        form.instance.save()
        form.instance.accounts.add(self.request.user)
        for account in new_account_list:
                form.instance.accounts.add(User.objects.get(username=account))
        form.instance.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['acc_list'] = obj.accounts.all().exclude(id=self.request.user.id)
        context['element_list'] = ProjectElement.objects.filter(project=obj).filter(parent=None)
        context['folder_list'] = Folder.objects.filter(project=obj).filter(parent=None)
        return context


@method_decorator(project_decorator, name='dispatch')
class ProjectDetail(DetailView):
    model = Project
    template_name = 'project_detail.html'
    query_pk_and_slug  = True
    pk_url_kwarg = 'project_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['element_list'] = ProjectElement.objects.filter(project=obj).filter(parent=None)
        context['folder_list'] = Folder.objects.filter(project=obj).filter(parent=None)
        return context


@login_required
def add_user(request):
    account_name = request.POST.get('acc_name')
    if (User.objects.filter(username=account_name).exists()) and not request.user.username == account_name:
        acc_id = User.objects.get(username=account_name).id
        data = {
        'exists' : acc_id
        }
    else:
        data = {
        'exists' : False
        }
    return JsonResponse(data)


        #views for elements:

@method_decorator(login_required, name='dispatch')
class NewFolder(CreateView):
    form_class = FolderForm
    template_name = 'new_element.html'
    success_url = '/projects/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_project_id'] = self.kwargs["project_id"]
        return kwargs

    def form_valid(self, form):
        form.instance.date_added = date.today()
        form.instance.project = Project.objects.get(id=self.kwargs["project_id"])
        form.instance.save()
        return super().form_valid(form)


@login_required
def folder_detail(request, project_id, folder_id):

    folder_list = Folder.objects.filter(parent__id = folder_id)
    element_list = ProjectElement.objects.filter(parent__id = folder_id)

    context_data = {
        'current_folder' : folder_id,
        'folder_list' : folder_list,
        'element_list' : element_list
    }

    if  request.GET.get('detail') == 'true':
        return render(request, 'load.html', context_data)
    else:
        return render(request, 'load_edit.html', context_data)


@method_decorator(login_required, name='dispatch')
class NewElement(CreateView):
    form_class = ElementForm
    template_name = 'new_element.html'
    success_url = '/projects/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_project_id'] = self.kwargs["project_id"]
        return kwargs

    def form_valid(self, form):
        form.instance.date_added = date.today()
        form.instance.project = Project.objects.get(id=self.kwargs["project_id"])
        form.instance.save()
        tag_list = self.request.POST.getlist('tags')
        for tag in tag_list:
            if not Tag.objects.filter(name=tag).exists():
                new_tag = Tag(name = tag)
                new_tag.save()
            form.instance.tags.add(Tag.objects.get(name=tag))
        form.instance.save()

        return super().form_valid(form)


def delete_element(request, project_id):
    return render(request, 'edit_project.html')


@login_required
def new_element(request, project_id):                                           # Creates a new project_element and adds it to the current project.

    if request.method == 'POST':

        form = ElementForm(project_id, request.POST, request.FILES)
        if form.is_valid():
            element_obj = form.cleaned_data
            name = element_obj['name']
            description = element_obj['description']
            folder = element_obj['parent']

            element = ProjectElement(name = name, description = description, date_added = date.today(), project = Project.objects.get(pk=project_id), parent = folder)
            if request.FILES:
                file = request.FILES['file']
                element.file = file

            element.save()

            return HttpResponseRedirect('/projects/' + str(project_id))
    else:
        form = ElementForm(project_id)

    return render(request, 'new_element.html', {'form': form})


@login_required
def element_detail(request, element_id, project_id):
        element = ProjectElement.objects.get(id=element_id)
        file_path = element.file.url
        print(file_path)
        context_data = {
            'element' : element,
            'file_path' : file_path

        }

        return render(request, 'element_detail.html', context_data)


    #other views:


class EditFolder(UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = 'edit_element.html'
    success_url = '/projects/{project_id}/edit'
    pk_url_kwarg = 'folder_id'

    def update_url(self):
        self.success_url += self.kwargs["project_id"] + '/edit'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_project_id'] = Project.objects.get(id=self.kwargs["project_id"])
        return kwargs



class EditElement(UpdateView):
    model = ProjectElement
    form_class = ElementForm
    template_name = 'edit_element.html'
    success_url = '/projects/{project_id}/edit'
    pk_url_kwarg = 'element_id'

    def update_url(self):
        self.success_url += self.kwargs["project_id"] + '/edit'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_project_id'] = Project.objects.get(id=self.kwargs["project_id"])
        return kwargs


def search(request):
    if request.method == 'POST':
        tag = request.POST.get('tag')
        return HttpResponseRedirect('results/' + tag)

    return render(request, 'search.html')

def results(request, tag):
    element_list = ProjectElement.objects.filter(tags__name = tag)
    return render(request, 'results.html', { 'element_list' : element_list})


@login_required
def home(request):
    return render(request, 'home.html', {'username' : request.user})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    return render(request, 'profile_edit.html', {'form': form})


    #views that don't require a login:


    #login, logout and register view

def landing_page(request):                 #creates a new user account

    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')


    if request.method == 'POST':
        form = AccountForm(request.POST)

        if form.is_valid():
            user_obj = form.cleaned_data
            username = user_obj['username']
            password = user_obj['password']
            email_address = user_obj['email_address']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email_address).exists()):  #checks if user/email already exists
                new_user = User.objects.create_user(username, email_address, password)
                new_user.save()
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/home')                         #creates user and account and links them together
            else:
                form = AccountForm()
    else:
        form = AccountForm()

    return render(request, 'landing_page.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_obj = form.cleaned_data
            username = user_obj['username']
            password = user_obj['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')

            else:
                return HttpResponseRedirect('/login')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login')


    #other views:

def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')
