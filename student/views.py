from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

from student.forms import ReportSubmitForm, UserProfileForm
from student.utils import is_student
from experiment.models import ExperimentReport, Experiment, Lesson


@login_required(login_url='student_index')
@is_student()
def experiment_information(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
        experiment_report = ExperimentReport.objects.get(
            student=request.user,
            experiment=experiment)
    except Experiment.DoesNotExist:
        raise Http404
    except ExperimentReport.DoesNotExist:
        experiment_report = None
    return render(request, 'student/experiment_info.html',
                  {'experiment': experiment,
                   'experiment_report': experiment_report})
    

@login_required(login_url='student_index')
def dashboard(request):
    return render(request, 'student/dashboard.html')


def index(request):
    try:
        isinstance(request.user, User)
    except AttributeError:
        return redirect('student_dashboard')
    return render(request, 'student/index.html')


@login_required(login_url='student_index')
@is_student()
def profile(request):
    return render(request, 'student/profile.html')


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
def submit_report(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
        Lesson.objects.get(experiment=experiment, students=request.user)
        experiment_report = ExperimentReport.objects.get(experiment=experiment,
                                                         student=request.user)
    except Experiment.DoesNotExist:
        raise Http404
    except Lesson.DoesNotExist:
        raise Http404
    except ExperimentReport.DoesNotExist:
        experiment_report = ExperimentReport(experiment=experiment,
                                             student=request.user)
    if request.method == 'POST':
        report_form = ReportSubmitForm(request.POST)
        if report_form.is_valid():
            experiment_report.title = report_form.cleaned_data['title']
            experiment_report.content = report_form.cleaned_data['content']
            experiment_report.save()
            # TO DO:success response
            return HttpResponse("success")
        else:
            raise Http404
    else:
        return render(request, "student/submit_report.html",
                      {"experiment_report": experiment_report})


@login_required(login_url='student_index')
@is_student()
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST,
                               instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('student_profile')


@login_required(login_url='student_index')
@is_student()
def pick_lesson_list(request):
    student = request.user
    lesson_list = Lesson.objects.filter(status=True)
    can_pick_lesson_list = lesson_list.exclude(students=student)
    return render(request, 'student/pick_lesson.html',
                  {'can_pick_lesson_list':can_pick_lesson_list})


@login_required(login_url='student_index')
@is_student()
def drop_lesson_list(request):
    student = request.user
    lesson_list = Lesson.objects.filter(status=True)
    can_drop_lesson_list = lesson_list.filter(students=student)
    return render(request, 'student/drop_lesson.html',
                  {'can_drop_lesson_list':can_drop_lesson_list})


@login_required(login_url='student_index')
@is_student()
def lesson_pick(request, lesson_id):
    student = request.user
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise Http404
    lesson.students.add(student)
    return redirect('pick_success')


@login_required(login_url='student_index')
@is_student()
def lesson_pick_success(request):
    return render(request, 'student/pick_success.html')


@login_required(login_url='student_index')
@is_student()
def lesson_drop(request, lesson_id):
    student = request.user
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise Http404
    lesson.students.remove(student)
    return redirect('drop_success')


@login_required(login_url='student_index')
@is_student()
def lesson_drop_success(request):
    return render(request, 'student/drop_success.html')


@login_required(login_url='student_index')
@is_student()
def list_lesson(request):
    student = request.user
    lesson_list = student.lesson_set.all()
    return render(request, 'student/lesson_list.html',
                  {'lesson_list':lesson_list})


@login_required(login_url='student_index')
@is_student()
def list_experiment(request):
    student = request.user
    experiment_list = Experiment.objects.filter(lesson__students=student)
    return render(request, 'student/experiment_list.html',
                  {'experiment_list':experiment_list})


@login_required(login_url='student_index')
@is_student()
def search_lesson(request):
    return render(request, 'student/search_lesson.html', {})


@login_required(login_url='student_index')
@is_student()
def search_lesson_result(request):
    lesson_list = {}
    if request.method == 'POST':
        lesson_name = request.POST.get('lesson_name', '')
        if lesson_name:
            lesson_list = Lesson.objects.filter(name__contains=lesson_name)
    return render(request, 'student/search_lesson_result.html',
                  {'lesson_list':lesson_list})


@login_required(login_url='student_index')
@is_student()
def experiment_information(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        raise Http404
    if experiment.lesson.status:
        return render(request, 'student/experiment_information.html',
                      {'experiment':experiment})
    raise Http404


@login_required(login_url='student_index')
@is_student()
def lesson_information(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id, status=True)
    except Lesson.DoesNotExist:
        raise Http404
    experiment_list = Experiment.objects.filter(lesson=lesson)
    return render(request, 'student/lesson_information.html',
                  {'lesson': lesson, 'experiment_list':experiment_list})
