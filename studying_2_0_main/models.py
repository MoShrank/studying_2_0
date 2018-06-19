from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 500)
    creation_date = models.DateField()
    accounts = models.ManyToManyField(Account)

    def __str__(self):
        return self.name

class Element(models.Model):
    name = models.CharField(max_length = 30)
    date_added = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default = 0)

    class Meta:
        abstract = True

class Folder(Element):
    self_elements = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name

class ProjectElement(Element):
    folder_element = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length = 500)
#    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.name
