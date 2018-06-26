from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

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

class Element(MPTTModel):
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
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

class ProjectElement(Element):
    description = models.CharField(max_length = 500)
    parent = TreeForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='children1')
#    file = models.FileField(upload_to='uploads/')
