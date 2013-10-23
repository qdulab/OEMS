from django.shortcuts import render
from teacher.utils import is_teacher
from experiment.models import Experiment
<<<<<<< HEAD
from experiment.models import LessonCategory, Lesson

def create_lesson_category(request):
    if request.method == 'POST':
        data = request.POST
        new_lesson_category = LessonCategory(name=data['lesson_category'])
        new_lesson_category.save()
        return render(request, 'experiment/create_succeed.html', {})
    else:
        return render(request, 'experiment/create_lesson_category.html', {})
=======
from django.contrib.auth.decorators import login_required
>>>>>>> a3b80c4b755495e3163f1ca094cb69383fe5213a

def display_experiment(request):
    experiment_list = Experiment.objects.all()
    return render(request, '../templates/experiment/display_experiments.html',
                  {experiment_list: experiment_list})

@login_required()
@is_teacher(redirect_url='index')
def create_experiment(request):

    return render(request, '../templates/experiment/create_experiment.html')
