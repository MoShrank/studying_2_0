from django.contrib import admin
from .models import Project, Account, ProjectElement, Folder
# Register your models here.

admin.site.register(Project)
admin.site.register(Account)
admin.site.register(ProjectElement)
admin.site.register(Folder)
