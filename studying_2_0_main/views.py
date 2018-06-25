from django.shortcuts import render, redirect
from django.template import loader
from .forms import AccountForm, LoginForm, ProjectForm, ElementForm, FolderForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from .models import Project, Account, ProjectElement, Folder
from datetime import date

# Create your views here.

def new_folder(request, project_id):
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = FolderForm(request.POST)
            if form.is_valid():
                folder_obj = form.cleaned_data
                name = folder_obj['name']

                if not(Folder.objects.filter(name=name).exists()):             #checks if elemet with equal name exists
                    fol = Folder(name = name, date_added = date.today(), project = Project.objects.get(pk=project_id))
                    fol.save()
                    return HttpResponseRedirect('/projects/' + str(project_id))
        else:
            form = FolderForm()


    return render(request, 'new_element.html', {'form': form})


def new_element(request, project_id):
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = ElementForm(project_id, request.POST)

            if form.is_valid():
                element_obj = form.cleaned_data
                name = element_obj['name']
                description = element_obj['description']

                ele = ProjectElement(name = name, description = description, date_added = date.today(), project = Project.objects.get(pk=project_id))
                ele.save()
                return HttpResponseRedirect('/projects/' + str(project_id))
        else:
            form = ElementForm(project_id)

    else:
        return redirect('/login')

    return render(request, 'new_element.html', {'form': form})


def element_detail(request, element_id, project_id):
        if request.user.is_authenticated:
            try:
                element = ProjectElement.objects.get(pk=element_id)
        #        element_list = ProjectElement.objects.filter(elements__id=element_id)
                context = {'element' : element}
            except:
                raise Http404("element does not exist")
            return render(request, 'element_detail.html', context)
        else:
            return redirect('/login')



def new_project(request):
    if request.user.is_authenticated:

        if request.method == 'POST':

            form = ProjectForm(request.POST)

            if form.is_valid():
                project_obj = form.cleaned_data
                name = project_obj['name']
                description = project_obj['description']
                account_str = project_obj['accounts']
                en = len(account_str) - 1
                account_str = account_str[:en]
                account_list = account_str.split(", ")

                print(account_list)
                if not(Project.objects.filter(name=name).exists()):             #checks if project with equal name exists
                    pro = Project(name = name, description = description, creation_date = date.today())
                    pro.save()
                    pro.accounts.add(Account.objects.get(user=request.user))
                    for acc in account_list:
                        pro.accounts.add(Account.objects.get(user__username=acc))
                        pro.save()
                    id = str(pro.id)
                    return HttpResponseRedirect('/projects/' + id)
        else:
            form = ProjectForm()

    else:
        return redirect('/login')

    return render(request, 'new_project.html', {'form': form})


def add_user(request):
    account = request.POST.get('acc_name')
    if (User.objects.filter(username=account).exists()) and not request.user.username == account:
        acc_id = User.objects.get(username=account).id
        data = {
        'exists' : acc_id
        }
    else:
        data = {
        'exists' : False
        }
    return JsonResponse(data)


def project_detail(request, project_id):
    if request.user.is_authenticated:
        try:
            project = Project.objects.get(pk=project_id)
            elements = ProjectElement.objects.filter(project=project)
            folder = Folder.objects.filter(project=project)
            context = {'project' : project, 'elements' : elements, 'folder' : folder}
        except:
            raise Http404("project does not exist")
        return render(request, 'project_detail.html', context)
    else:
        return redirect('/login')


def welcome(request):
    if request.user.is_authenticated:
        username = request.user.username
        context = {'username' : username}
        return render(request, 'welcome.html', context)
    else:
        return redirect('/login')


def home(request):
    return HttpResponseRedirect('/')


def projects(request):
    current_user = request.user
    if current_user.is_authenticated:
        project_list = Project.objects.filter(accounts__user__username=current_user.username)
        context = {'project_list' : project_list}
        return render(request, 'projects.html', context)
    else:
        return HttpResponseRedirect('/login')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_obj = form.cleaned_data
            username = user_obj['username']
            password = user_obj['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                context = {'username' : username}
                return render(request, 'welcome.html', context)
            else:
                return HttpResponseRedirect('/login')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login')


def landing_page(request):                  #creates a new user account

    if request.user.is_authenticated:
        return HttpResponseRedirect('/welcome')

    if request.method == 'POST':
        form = AccountForm(request.POST)

        if form.is_valid():
            user_obj = form.cleaned_data
            username = user_obj['username']
            password = user_obj['password']
            email_address = user_obj['email_address']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email_address).exists()):  #checks if user/email already exists
                u = User.objects.create_user(username, email_address, password)
                a = Account(user = u)
                a.save()
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/projects')
            else:
                form = AccountForm()
    else:
        form = AccountForm()

    return render(request, 'landing_page.html', {'form': form})
