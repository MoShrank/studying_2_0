from .models import Project, Account
from django.core.exceptions import PermissionDenied


def user_is_project_author(function):
    def wrap(request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['project_id'])
        account_set = project.accounts.all()
        account = Account.objects.get(user=request.user)
        if account in account_set:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
