# Create your views here.
from django.shortcuts import render
from teacher.utils import is_teacher
from experiment.models import Experiment
from django.contrib.auth.decorators import login_required

def display_experiment(request):
    experiment_list = Experiment.objects.all()
    return render(request, '../templates/experiment/display_experiments.html',
                  {experiment_list: experiment_list})

@login_required()
@is_teacher(redirect_url='index')
def create_experiment(request):

    return render(request, '../templates/experiment/create_experiment.html')
