from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from teacher.forms import TeacherForm, TeacherProfileForm
from teacher.models import Teacher, TeacherProfile
from teacher.utils import is_teacher


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            teacher = authenticate(username=username, password=password)
            if teacher is not None and isinstance(teacher, Teacher):
                login(request, teacher)
                return redirect('teacher_dashboard')
    return redirect('teacher_index')


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def sign_out(request):
    logout(request)
    return redirect('teacher_index')


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def teacher_profile(request):
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("edit_success")
    else:
        form = TeacherProfileForm(instance=request.user.profile)
    return render(request, 'teacher/profile.html', {'form':form})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def edit_success(request):
    return render(request, 'teacher/edit_success.html', {})
