from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from teacher.models import Teacher
from teacher.utils import is_teacher
from teacher.forms import TeacherForm


@login_required()
@is_teacher()
def dashboard(request):
    return render(request, 'teacher/dashboard.html')


def index(request):
    if hasattr(request, 'user') and isinstance(request.user, Teacher):
        return redirect('teacher_dashboard')
    return render(request, 'teacher/index.html')


def sign_in(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = authenticate(username=form.cleaned_data['username'],
                                   password=form.cleaned_data['password'])
            if teacher is not None and isinstance(teacher, Teacher):
                login(request, teacher)
                return redirect('teacher_dashboard')
    return redirect('teacher_index')

#TODO  add:(login_url='/teacher/login')
@login_required()
def sign_out(request):
    logout(request)
    return redirect('teacher_index')
