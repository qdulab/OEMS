from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render

from student.forms import UserProfileForm
from student.models import UserProfile
from student.utils import is_student


@login_required(login_url='student_index')
@is_student()
def dashboard(request):
    return render(request, 'student/dashboard.html')


def index(request):
    try:
        isinstance(request.user, User)
    except AttributeError:
        return redirect('student_dashboard')
    return render(request, 'student/index.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        student = authenticate(username=username, password=password)
        if isinstance(student, User):
            login(request, student)
            return redirect('student_dashboard')
    return redirect('student_index')


@login_required(login_url='student_index')
@is_student()
def sign_out(request):
    logout(request)
    return redirect('student_index')


@login_required(login_url='student_index')
@is_student()
def update_profile(request):
    try:
        profile = UserProfile.objects.get(id=request.user.id,
                                       student=request.user)
    except User.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            profile.school_id = form.cleaned_data['school_id']
            profile.grade = form.cleaned_data['grade']
            profile.major = form.cleaned_data['major']
            profile.class_num = form.cleaned_data['class_num']
            profile.phone_num = form.cleaned_data['phone_num']
            profile.save()
            return redirect('created_success')
        else:
            raise Http404
    else:
        form = UserProfile.objects.filter(student=request.user)[0]
        return render(request, 'student/update_profile.html',
                      {'form': form})

@login_required(login_url='student_index')
@is_student()
def view_profile(request):
    form = UserProfile.objects.get_or_create(student=request.user)[0]
    return render(request, 'student/profile.html',
                  {'form': form})
