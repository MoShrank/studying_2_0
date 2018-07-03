from django.shortcuts import render, redirect
from django.template import loader
from .forms import AccountForm, LoginForm, ProjectForm, ElementForm, FolderForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from .models import Project, Account, ProjectElement, Folder
from datetime import date
from django.contrib.auth.decorators import login_required

    #views that require a login:


    #views for project:

@login_required
def new_project(request):
    if request.method == 'POST':

        form = ProjectForm(request.POST)

        if form.is_valid():
            project_obj = form.cleaned_data
            name = project_obj['name']
            description = project_obj['description']
            account_list = request.POST.getlist('accounts')

            if not(Project.objects.filter(name=name).exists()):             #checks if project with equal name exists
                project = Project(name = name, description = description, creation_date = date.today())
                project.save()
                project.accounts.add(Account.objects.get(user=request.user))
                for account in account_list:
                    project.accounts.add(Account.objects.get(user__username=account))
                    project.save()
                id = str(project.id)
                return HttpResponseRedirect('/projects/' + id)
    else:
        form = ProjectForm()

    return render(request, 'new_project.html', {'form': form})


@login_required
def edit_project(request, project_id):
    if request.method == 'POST':
        if form.is_valid():
            project = form.cleaned_data
            name = project_obj['name']
            description = project_obj['description']

            if not(Project.objects.filter(name=name).exists()):             #checks if project with equal name exists
                pro = Project(name = name, description = description)
                pro.save()
                id = str(pro.id)
                return HttpResponseRedirect('/projects/' + id)

    else:
        pro = Project.objects.get(id=project_id)
        form = ProjectForm(initial={'name': pro.name, 'description' : pro.description})


    return render(request, 'new_project.html', {'form': form})


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


@login_required
def project_detail(request, project_id):
    account = Account.objects.get(user=request.user)
    project = Project.objects.get(id=project_id)
    if project.accounts.get(id=account.id):

        try:
            project = Project.objects.get(pk=project_id)
            elements = ProjectElement.objects.filter(project=project)
            folder = Folder.objects.filter(project=project)
            context = {'project' : project, 'elements' : elements, 'folder' : folder}
            return render(request, 'project_detail.html', context)
        except:
            raise Http404("project does not exist")

    else:
        return HttpResponseRedirect('/projects')


@login_required
def projects(request):
    current_user = request.user
    if current_user.is_authenticated:
        project_list = Project.objects.filter(accounts__user__username=current_user.username)
        return render(request, 'projects.html', {'project_list' : project_list})
    else:
        return HttpResponseRedirect('/login')


        #views for elements:


@login_required
def new_folder(request, project_id):                                            # Creates a new folder and adds it to the current project.
    if request.method == 'POST':
        form = FolderForm(project_id, request.POST)
        if form.is_valid():
            folder_obj = form.cleaned_data
            name = folder_obj['name']

            if not(Folder.objects.filter(name=name).exists()):
                folder = Folder(name = name, date_added = date.today(), project = Project.objects.get(pk=project_id))
                folder.save()
                return HttpResponseRedirect('/projects/' + str(project_id))
    else:
        form = FolderForm(project_id)

    return render(request, 'new_element.html', {'form': form})


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
                element.file = request.FILES['file']
            element.save()

            return HttpResponseRedirect('/projects/' + str(project_id))
    else:
        form = ElementForm(project_id)

    return render(request, 'new_element.html', {'form': form})


@login_required
def element_detail(request, element_id, project_id):
        element = ProjectElement.objects.get(id=element_id)
        name = element.name
        description = element.description
        data = {
            'name' : name,
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
