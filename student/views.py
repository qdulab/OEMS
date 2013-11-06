from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import Http404

from experiment.models import Lesson, Experiment


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
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise Http404
    lesson.students.remove(student)
    return redirect('drop_success')


def lesson_drop_success(request):
    return render(request, 'student/drop_success.html')


def list_lesson(request):
    student = request.user
    lesson_list = student.lesson_set.all()
    return render(request, 'student/lesson_list.html', {'lesson_list':lesson_list})


def list_experiment(request):
    student = request.user
    experiment_list = Experiment.objects.filter(lesson__students=student)
    return render(request, 'student/experiment_list.html', {'experiment_list':experiment_list})


def search_lesson(request):
    return render(request, 'student/search_lesson.html', {})


def search_lesson_result(request):
    lesson_list = {}
    if request.method == 'POST':
        lesson_name = request.POST.get('lesson_name', '')
        if lesson_name is not None:
            lesson_list = Lesson.objects.filter(name__contains=lesson_name)
    return render(request, 'student/search_lesson_result.html', {'lesson_list':lesson_list})

def experiment_information(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        raise Http404
    if experiment.lesson.status == True:
        return render(request, 'student/experiment_information.html',
                     {'experiment':experiment})
    raise Http404

def lesson_information(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise Http404
    if lesson.status == True:
        experiment_list = Experiment.objects.filter(lesson=lesson)
        return render(request, 'student/lesson_information.html',
                     {'lesson': lesson, 'experiment_list':experiment_list})
    raise Http404
