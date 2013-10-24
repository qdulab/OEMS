from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from experiment.models import Experiment
from experiment.models import LessonCategory, Lesson
from teacher.models import Teacher
from teacher.utils import is_teacher


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_lesson_category(request):
    if request.method == 'POST':
        lesson_category = request.POST.get('lesson_category', None)
        if lesson_category:
            LessonCategory.objects.create(name=lesson_category)
            return render(request, 'experiment/create_succeed.html', {})
        else:
            return redirect('create_lesson_category')
    else:
        return render(request, 'experiment/create_lesson_category.html', {})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_lesson(request):
    if request.method == 'POST':
        lesson_name = request.POST.get('lesson_name')
        if lesson_name:
            lesson_category = request.POST.get('lesson_category', None)
            category = LessonCategory.objects.get(name=lesson_category)
            lesson_info = request.POST.get('lesson_info')
            teacher_name = request.user.get_username()
            teacher = Teacher.objects.get(username=teacher_name)
            Lesson.objects.create(name=lesson_name, category=category,
                                  teacher=teacher, info=lesson_info,
                                  status=True)
            return render(request, 'experiment/create_succeed.html', {})
        else:
            return redirect('create_lesson')
    else:
        lesson_categories = LessonCategory.objects.all().values('name')
        return render(request, 'experiment/create_lesson.html',
                     {'lesson_categories': lesson_categories})


#@login_required()
#@is_teacher('index')
def display_experiment(request):
    experiment_list = Experiment.objects.all()
    return render(request, 'experiment/display_experiments.html',
                  {'experiment_list': experiment_list})

#@login_required()
#@is_teacher('index')
def create_experiment(request):
    if request.method == 'POST' :
        name = request.POST.get("experiment_name", None)
        content = request.POST.get("experiment_content", None)
        deadline = request.POST.get("deadline", None)
        remark = request.POST.get("remark", None)
#        weight = request.POST.get("weight", None)
        experiment = Experiment(name=name, content=content, deadline=deadline, remark=remark,  lesson=experiment_lesson)
        experiment.save()
        return render(request, 'experiment/create_experiment_success.html')
    else:
        return render(request, 'experiment/create_experiment.html')
