from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404

from experiment.models import Experiment
from experiment.models import LessonCategory, Lesson
from teacher.models import Teacher
from teacher.utils import is_teacher


def created_success(request):
    return render(request, 'teacher/created_success.html', {})



@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_experiment_success(request):
    return render(request, 'teacher/create_experiment_success.html', {})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_lesson_category(request):
    lesson_category = request.POST.get('lesson_category', None)
    if lesson_category:
        LessonCategory.objects.create(name=lesson_category)
        return redirect('created_success')
    else:
        return render(request, 'teacher/create_lesson_category.html', {})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
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
        return redirect('created_success')
    else:
        lesson_categories = LessonCategory.objects.all().values('name')
        return render(request, 'teacher/create_lesson.html',
                      {'lesson_categories': lesson_categories})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def lesson_information(request, lesson_id):
    teacher = request.user
    try:
        lesson = Lesson.objects.get(id=lesson_id, teacher=teacher)
    except Lesson.DoesNotExist:
        raise Http404
    experiment_list = Experiment.objects.filter(lesson=lesson)
    return render(request, 'teacher/experiment_information.html',
                  {'experiment_list': experiment_list,
                   'lesson': lesson,
                   'lesson_id': lesson_id
                  })


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def lesson_list(request):
    teacher = request.user
    lesson_list = Lesson.objects.filter(teacher=teacher)
    return render(request, 'teacher/lesson_list.html',
                  {'lesson_list': lesson_list})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_experiment(request, lesson_ide):
    name = request.POST.get('experiment_name', None)
    username = request.user.username
    teacher = Teacher.objects.get(username=username)
    lesson_list = Lesson.objects.filter(teacher=teacher)
    if name:
        content = request.POST.get("experiment_content", None)
        deadline = request.POST.get("deadline", None)
        remark = request.POST.get("remark", None)
#        weight = request.POST.get("weight", None)
        lesson_id = request.POST.get("lesson_id", None)
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return render(request, "teacher/base.html")
        experiment = Experiment(name=name, content=content, deadline=deadline,
                                remark=remark, lesson=lesson)
        experiment.save()
        return redirect('create_experiment_success')
    else:
        return render(request, 'teacher/create_experiment.html',
                      {"lesson_list": lesson_list, "lesson_id": lesson_ide})
