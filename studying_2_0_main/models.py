from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 500)
    creation_date = models.DateField()
    accounts = models.ManyToManyField(User)
    slug = models.SlugField(max_length = 30)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

class Element(models.Model):
    name = models.CharField(max_length = 30)
    date_added = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def set_parents(self, list):
        for element in list:
            element.parent = self.parent
            element.save()

    def __str__(self):
        return self.name

class Folder(Element):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

class ProjectElement(Element):
    description = models.CharField(max_length = 500)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
