# Create your views here.
from django.shortcuts import render

from experiment.models import Experiment


def display_experiment(request):
    experiment_list = Experiment.objects.all()
    return render(request, '../templates/experiment/display_experiments.html',
                  {experiment_list: experiment_list})

