from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils import simplejson

from experiment.models import ExperimentReport
from teacher.forms import ReportEvaluateForm, TeacherForm, TeacherProfileForm
from teacher.models import Teacher
from teacher.utils import is_teacher


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def dashboard(request):
    return render(request, 'teacher/dashboard.html')


def index(request):
    try:
        if isinstance(request.user, Teacher):
            return redirect('teacher_dashboard')
    except AttributeError:
        return render(request, 'teacher/index.html')
    logout(request)
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
def experiment_report_evaluate(request, experiment_report_id):
    try:
        experiment_report = ExperimentReport.objects.get(
            id=experiment_report_id)
    except ExperimentReport.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = ReportEvaluateForm(request.POST)
        if form.is_valid():
            experiment_report.score = form.cleaned_data['score']
            experiment_report.comment = form.cleaned_data['comment']
            experiment_report.save()
            return HttpResponse("success")
        else:
            # TO DO:form error tip
            raise Http404
    else:
        return render(request, 'teacher/experiment_report_evaluate.html',
                      {'experiment_report': experiment_report})


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
            json = {"status" : 1,
                    "address" : form.cleaned_data['address'],
                    "mobile" : form.cleaned_data['mobile'],
                    "QQ" : form.cleaned_data['QQ'],
                    "blog" : form.cleaned_data['blog']}
            return HttpResponse(simplejson.dumps(json))
    else:
        form = TeacherProfileForm(instance=request.user.profile)
    return render(request, 'teacher/profile.html', {'form': form})
