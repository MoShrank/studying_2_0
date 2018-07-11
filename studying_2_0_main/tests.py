from django.test import TestCase
from .models import Account, Project
from datetime import date

# Create your tests here.



class ProjectModelTest(TestCase):

    accounts = Accounts.objects.all()

    def setUp(self):

        f = Project.objects.create(name = 'test1', description = '.', creation_date = date.today())
        f.accounts.set(accounts)
        f = Project.objects.create(name = 'test2', description = '.', creation_date = date.today())
        f.accounts.add(Account.objects.get(user__username='shrank'))

    def test_create_projects(self):
        f = Project.objects.get(name='test1')
        s = Projects.objects.get(name='test2')
