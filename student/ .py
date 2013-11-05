from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

from experiment.models import Lesson


@login_required(login_url='student_index')
def dashboard(request):
    return render(request, 'student/dashboard.html', {})

def index(request):
    if hasattr(request, 'user') and isinstance(request.user, User):
        return redirect('student_dashboard')
    return render(request, 'student/index.html', {})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        student = authenticate(username=username, password=password)
        if student is not None and isinstance(student, User):
            login(request, student)
            return redirect('student_dashboard')
    return redirect('student_dashboard')

@login_required(login_url='student_index')
def sign_out(request):
    logout(request)
    return redirect('student_index')


def pick(request):
    student = request.user
    lesson_list = Lesson.objects.filter(status=True)
    drop_list = lesson_list.exclude(students=student)
    return render(request, 'student/pick.html', {'drop_list':drop_list})

def drop(request):
    student = request.user
    lesson_list = Lesson.objects.filter(status=True)
    pick_list = lesson_list.filter(students=student)
    return render(request, 'student/drop.html', {'pick_list':pick_list})


def lesson_pick(request, lesson_id):
    student = request.user
    lesson = Lesson.objects.get(id=lesson_id)
    lesson.students.add(student)
    return redirect('pick_success')

def lesson_pick_success(request):
    return render(request, 'student/pick_success.html')

def lesson_drop(request, lesson_id):
    student = request.user
    lesson = Lesson.objects.get(id=lesson_id)
    lesson.students.remove(student)
    return redirect('drop_success')

def lesson_drop_success(request):
    return render(request, 'student/drop_success.html')

def list_lesson(request):
    student = request.user
    lesson_list = student.lesson_set.all()
    return render(request, 'student/lesson_list.html', {'lesson_list':lesson_list})


