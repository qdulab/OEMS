from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from experiment.models import Experiment
from experiment.models import LessonCategory, Lesson
from teacher.models import Teacher
from teacher.utils import is_teacher


def created_success(request):
    return render(request, 'teacher/created_success.html', {})

#@login_required(login_url='teacher')
#@is_teacher(redirect_url='')
def create_lesson_category(request):
    lesson_category = request.POST.get('lesson_category', None)
    if lesson_category:
        LessonCategory.objects.create(name=lesson_category)
        return redirect('created_success')
    else:
        return render(request, 'teacher/create_lesson_category.html', {})


#@login_required(login_url='teacher')
#@is_teacher(redirect_url='')
def create_lesson(request):
    lesson_name = request.POST.get('lesson_name', None)
    if lesson_name:
        lesson_category = request.POST.get('lesson_category', None)
        try:
            category = LessonCategory.objects.get(name=lesson_category)
        except LessonCategory.DoesNotExist:
            pass
        lesson_info = request.POST.get('lesson_info', None)
        teacher = request.user
        Lesson.objects.create(name=lesson_name, category=category,
                              teacher=teacher, info=lesson_info,
                              status=True)
        return redirect('create_succeed')
    else:
        lesson_categories = LessonCategory.objects.all().values('name')
        return render(request, 'teacher/create_lesson.html',
                      {'lesson_categories': lesson_categories})


#@login_required(login_url='teacher')
#@is_teacher(redirect_url='')
def display_experiment(request):
#    username = request.user.username
#    teacher = Teacher.objects.get(username=username)
    experiment_list = Experiment.objects.all()
    return render(request, 'teacher/display_experiments.html',
                  {'experiment_list': experiment_list})

#@login_required(login_url='teacher')
#@is_teacher(redirect_url='')
def display_lessons(request):
    #teacher = Teacher.objects.get(username=requset.user.get('usertname',None), None)
    lesson_list = Lesson.objects.all()
    return render(request, 'teacher/display_lessons.html',
                  {'lesson_list': lesson_list})


#@login_required(login_url='teacher')
#@is_teacher(redirect_url='')
def create_experiment(request):
    name = request.POST.get('experiment_name', None)
    username = request.user.username
    teacher = Teacher.objects.get(username=username)
    lesson_ls = Lesson.objects.filter(teacher=teacher)
    if name:
        content = request.POST.get("experiment_content", None)
        deadline = request.POST.get("deadline", None)
        remark = request.POST.get("remark", None)
#        weight = request.POST.get("weight", None)
        lesson_id = request.POST.get("lesson_id", None)
        try:
            lesson_object = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return render(request, "teacher/base.html")
        except ValueError:
            return render(request, "teacher/dashboard.html")
        experiment = Experiment(name=name, content=content, deadline=deadline,
                                remark=remark, lesson=lesson_object)
        experiment.save()
        return render(request, 'teacher/create_experiment_success.html')
    else:
        return render(request,'teacher/create_experiment.html',
                {"lesson_list": lesson_ls})

