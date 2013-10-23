from django.http import HttpResponse
from django.shortcuts import redirect

from teacher.models import Teacher

def is_teacher(function, redirect_url=''):
    """This is a view decorator, to valid if teacher has login
       login: call function as normal
       not login: rediretu to the redirect_url, if redirect_url is None,
                  will return a HttpResponse which body is "hehe"
    """
    def wrap(request, *args, **kwargs):
        try:
            user = request.user
        except AttributeError:
            if redirect_url:
                return redirect(redirect_url)
            return HttpResponse('hehe')

        if isinstance(user, Teacher):
            return function(request, *args, **kwargs)
        else:
            if redirect_url:
                return redirect(redirect_url)
            return HttpResponse('hehe')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
