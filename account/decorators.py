from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from . models import *
from django.shortcuts import redirect, render


def role_required(allowed_roles=["is_admin"]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if CustomUser in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect ("/")
        return wrap
    return decorator 

