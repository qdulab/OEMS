from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from student.forms import ReportSubmitForm

from experiment.models import ExperimentReport, Experiment


@login_required(login_url='student_index')
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
def sign_out(request):
    logout(request)
    return redirect('student_index')


@login_required(login_url='student_index')
def submit_report(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
        experiment_report = ExperimentReport.objects.get(experiment=experiment,
                                                         student=request.user)
    except Experiment.DoesNotExist:
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
