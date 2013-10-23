from django.shortcuts import render

from experiment.models import Experiment
from experiment.models import LessonCategory, Lesson

def create_lesson_category(request):
    if request.method == 'POST':
        data = request.POST
        new_lesson_category = LessonCategory(name=data['lesson_category'])
        new_lesson_category.save()
        return render(request, 'experiment/create_succeed.html', {})
    else:
        return render(request, 'experiment/create_lesson_category.html', {})

def display_experiment(request):
    experiment_list = Experiment.objects.all()
    return render(request, '../templates/experiment/display_experiments.html',
                  {experiment_list: experiment_list})

