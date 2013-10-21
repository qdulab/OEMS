from django.http import HttpResponse
from django.shortcuts import redirect

from teachers.models import Teacher

def is_teacher(function, redirect_url=''):
    def wrap(request, *args, **kwargs):
        if isinstance(request.user, Teacher):
            return function(request, *args, **kwargs)
        else:
            if redirect_url:
                return redirect(redirect_url)
            return HttpResponse('hehe')
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap
