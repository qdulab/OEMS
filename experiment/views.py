from django.shortcuts import render
from experiment.models import Experiment
from experiment.models import LessonCategory, Lesson
from teacher.models import Teacher


def index(request):
    return render(request, '../templates/two_columns.html')

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

#@login_required()
#@is_teacher('index')
def create_experiment(request):
    if request.method == 'POST' :
        experiment_name = request.POST.get("experiment_name")
        experiment_content = request.POST.get("experiment_content")
        experiment_deadline = request.POST.get("deadline")
        experiment_remark = request.POST.get("remark")
        experiment_weight = request.POST.get("weight")
        experiment_lesson = Lesson.objects.filter(id=request.POST.get("lesson_id"))
        experiment = Experiment(name=experiment_name, content=experiment_content, deadline=experiment_deadline, remark=experiment_remark, weight=experiment_weight, lesson=experiment_lesson)
        experiment.save()
    else:
        return render(request, '../templates/experiment/create_experiment.html')
