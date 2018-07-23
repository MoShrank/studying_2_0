from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 500)
    creation_date = models.DateField()
    accounts = models.ManyToManyField(Account)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length = 30)

class Element(models.Model):
    name = models.CharField(max_length = 30)
    date_added = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Folder(Element):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

class ProjectElement(Element):
    description = models.CharField(max_length = 500)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='uploads/', blank = True, null = True)
    tags = models.ManyToManyField(Tag)
