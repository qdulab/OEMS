from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from teacher.models import Teacher
from teacher.utils import is_teacher


@login_required()
@is_teacher()
def dashboard(request):
    return render(request, 'teacher/dashboard.html')


def index(request):
    return render(request, 'teacher/index.html')

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
    	teacher = authenticate(username=username, password=password)
        if teacher is not None and isinstance(teacher, Teacher):
            login(request, teacher)
            return redirect('teacher_dashboard')
    return redirect('teacher_index')

#TODO  add:(login_url='/teacher/login')
@login_required()
def sign_out(request):
    logout(request)
    return redirect('teacher_index')
