from django.http import HttpResponse

from teachers.models import Teacher

def is_teacher(function):
    def wrap(request, *args, **kwargs):
        if isinstance(request.user, Teacher):
            return function(request, *args, **kwargs)
        else:
            return HttpResponse('hehe')
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap
