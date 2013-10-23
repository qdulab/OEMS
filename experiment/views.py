from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from teacher.utils import is_teacher
from experiment.models import Experiment
from experiment.models import LessonCategory, Lesson
from teacher.models import Teacher

#@login_required()
#@is_teacher(redirect_url='')
def create_lesson_category(request):
    if request.method == 'POST':
        lesson_category = request.POST.get('lesson_category', None)
        LessonCategory.objects.create(name=lesson_category)
        return render(request, 'experiment/create_succeed.html', {})
    else:
        category = LessonCategory.objects.all()
        return render(request, 'experiment/create_lesson_category.html',
                     {'lesson_category': category})
def create_lesson(request):
    if request.method == 'POST':
        lesson_category = request.POST.get('lesson_category', None)
        category = LessonCategory.objects.get(name=lesson_category)
        lesson_name = request.POST.get('lesson_name')
        lesson_info = request.POST.get('lesson_info')
        teacher_name = request.user.get_username()
        teacher = Teacher.objects.get(name=teacher_name)
        Lesson.objects.create(name=lesson_name, category=category,
                              teacher=teacher, info=lesson_info, status=True)
        return render(request, 'experiment/create_succeed.html', {})
    else:
        lesson_categories = LessonCategory.objects.all().values('name')
        return render(request, 'experiment/create_lesson.html',
                     {'lesson_categories': lesson_categories})


def display_experiment(request):
    experiment_list = Experiment.objects.all()
    return render(request, '../templates/experiment/display_experiments.html',
                  {experiment_list: experiment_list})

@login_required()
@is_teacher(redirect_url='index')
def create_experiment(request):

    return render(request, '../templates/experiment/create_experiment.html')
