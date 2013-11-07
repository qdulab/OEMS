from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect


def is_student(redirect_url=''):
    """
    This is a view decorator, to valid if user has login
    login: call function as normal
    not login: redirect to the redirect_url, if redirect_url is None,
               will return a HttpResponse which body is "bad"
    """
    def decorate(function):
        def wrapper(request, *args, **kwargs):
            try:
                user = request.user
            except AttributeError:
                if redirect_url:
                    return redirect(redirect_url)
                return HttpResponse("bad")

            if isinstance(user, User):
                return function(request, *args, **kwargs)
            else:
                if redirect_url:
                    return redirect(redirect_url)
                return HttpResponse("bad")

        wrapper.__doc__ = function.__doc__
        wrapper.__name__ = function.__name__
        return wrapper
    return decorate
