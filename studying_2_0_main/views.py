from django.shortcuts import render, redirect
from django.template import loader
from .forms import AccountForm, LoginForm, ProjectForm, ElementForm, FolderForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from .models import Project, Account, ProjectElement, Folder, Tag
from datetime import date
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from .decorators import user_is_project_author
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


project_decorator = [login_required, user_is_project_author]


    #views that require a login:


    #views for project:

@method_decorator(login_required, name='dispatch')
class Projects(ListView):
    context_object_name = 'project_list'
    template_name = 'projects.html'

    def get_queryset(self):
        return Project.objects.filter(accounts__user__username=self.request.user)

@method_decorator(login_required, name='dispatch')
class NewProject(CreateView):
    form_class = ProjectForm
    template_name = 'new_project.html'
    success_url = '/projects/'

    def form_valid(self, form):
        form.instance.creation_date = date.today()
        form.instance.save()
        form.instance.accounts.add(Account.objects.get(user=self.request.user))
        account_list = self.request.POST.getlist('accounts')
        for account in account_list:
            form.instance.accounts.add(Account.objects.get(user__username=account))
        form.instance.save()

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EditProject(UpdateView):
    form_class = ProjectForm
    template_name = 'edit_project.html'
    success_url = '/projects/'

    def get_object(self, queryset=None):
        return Project.objects.get(id=self.kwargs["project_id"])

    def update_url(self, project_id):
        self.success_url += project_id + '/'

    def form_valid(self, form):
        new_account_list = self.request.POST.getlist('accounts')
        obj = self.get_object()
        obj.accounts.clear()
        form.instance.save()
        form.instance.accounts.add(Account.objects.get(user = self.request.user))
        for account in new_account_list:
                form.instance.accounts.add(Account.objects.get(user__username=account))
        form.instance.save()

        self.update_url(str(obj.id))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acc_list'] = self.get_object().accounts.exclude(user = self.request.user)
        return context


@method_decorator(project_decorator, name='dispatch')
class ProjectDetail(DetailView):
    template_name = 'project_detail.html'

    def get_object(self, queryset=None):
        return Project.objects.get(id=self.kwargs["project_id"])

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

@login_required
class NewFolder(CreateView):
    form_class = FolderForm

    def form_valid(self, form):

        return super().form_valid(form)

@login_required
def new_folder(request, project_id):                                            # Creates a new folder and adds it to the current project.
    if request.method == 'POST':
        form = FolderForm(project_id, request.POST)
        if form.is_valid():
            folder_obj = form.cleaned_data
            name = folder_obj['name']
            parent = folder_obj['parent']

            if not(Folder.objects.filter(name=name).exists()):
                folder = Folder(name = name, date_added = date.today(), project = Project.objects.get(pk=project_id), parent=parent)
                folder.save()
                return HttpResponseRedirect('/projects/' + str(project_id))
    else:
        form = FolderForm(project_id)

    return render(request, 'new_element.html', {'form': form})


@login_required
def folder_detail(request, project_id, folder_id):

    folder_list = Folder.objects.filter(parent__id = folder_id)
    element_list = ProjectElement.objects.filter(parent__id = folder_id)

    context_data = {
        'current_folder' : folder_id,
        'folder_list' : folder_list,
        'element_list' : element_list
    }
    return render(request, 'load.html', context_data)
    #return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class NewElement(CreateView):
    form_class = ElementForm
    template_name = 'new_element.html'
    success_url = '/projects/'

    def get_object(self, queryset=None):
        return Project.objects.get(id=self.kwargs["project_id"])


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_project_id'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.instance.date_added = date.today()
        form.instance.save()
        tag_list = self.request.POST.getlist('tags')
        print(tag_list)
        print('hi')
        for tag in tag_list:
            if not Tag.objects.filter(name=tag).exists():
                new_tag = Tag(name = tag)
                new_tag.save()
            form.instance.tags.add(Tag.objects.get(name=tag))
        form.instance.save()

        return super().form_valid(form)



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
        description = element.description
        data = {
            'file_path' : file_path,
            'description' : description
        }
        return JsonResponse(data)

        #    try:
        #        element = ProjectElement.objects.get(pk=element_id)
        #        element_list = ProjectElement.objects.filter(elements__id=element_id)
        #        context = {'element' : element}
        #    except:
        #        raise Http404("element does not exist")
        #    return render(request, 'element_detail.html', context)
        #else:
        #    return redirect('/login')



    #other views:


@login_required
def home(request):
    return render(request, 'home.html', {'username' : request.user})


@login_required
def profile(request):

        return HttpResponseRedirect('/login')


    #views that don't require a login:


    #login, logout and register view

def landing_page(request):                  #creates a new user account

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
                account = Account(user = new_user)
                account.save()
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
                print('hi')
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

def search(request):
    if request.method == 'POST':
        tag = request.POST.get('tag')
        return HttpResponseRedirect('results/' + tag)

    return render(request, 'search.html')

def results(request, tag):
    element_list = ProjectElement.objects.filter(tags__name = tag)
    return render(request, 'results.html', { 'element_list' : element_list})
