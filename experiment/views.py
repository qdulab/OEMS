from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404

from experiment.models import Experiment, LessonCategory, Lesson
from experiment.forms import ExperimentForm, LessonCategoryForm
from experiment.forms import LessonForm
from teacher.utils import is_teacher


def created_success(request):
    return render(request, 'teacher/created_success.html', {})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_experiment_success(request, lesson_id):
    return render(request, 'teacher/create_experiment_success.html',
                  {'lesson_id': lesson_id})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_lesson_category(request):
    if request.method == 'POST':
        form = LessonCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            LessonCategory.objects.create(name=name)
        return redirect('created_success')
    return render(request, 'teacher/create_lesson_category.html',)


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_lesson(request):
    if request.method == 'POST':
        form = LessonForm(data=request.POST)
        if form.is_valid():
            teacher = request.user
            form.save(teacher=teacher)
            return redirect('created_success')
        else:
            return render(request,
                          'teacher/create_lesson.html', {})
    else:
        categories = LessonCategory.objects.all()
        return render(request, 'teacher/create_lesson.html',
                      {'categories': categories})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_experiment(request, lesson_id):
    lesson_list = Lesson.objects.filter(teacher=request.user)
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            content = form.cleaned_data['content']
            deadline = form.cleaned_data['deadline']
            info = form.cleaned_data['information']
            try:
                lesson = Lesson.objects.get(id=lesson_id, teacher=request.user)
            except Lesson.DoesNotExist:
                return render(request, "base.html")
            experiment = Experiment(
                name=name, content=content, deadline=deadline,
                remark=info, lesson=lesson)
            experiment.save()
            return redirect('create_experiment_success', lesson_id=lesson_id)
        else:
            render(request, "base.html")
    else:
        return render(request, 'teacher/create_experiment.html',
                      {"lesson_list": lesson_list})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def delete_experiment(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        raise Http404
    if experiment.lesson.teacher == request.user:
        experiment.delete()
        return redirect('delete_success')
    else:
        return Http404


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def delete_lesson(request, lesson_id):
    try:
        Lesson.objects.get(id=lesson_id, teacher=request.user).delete()
    except Experiment.DoesNotExist:
        raise Http404
    return redirect('delete_success')


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def delete_success(request):
    return render(request, 'teacher/delete_success.html', {})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def experiment_information(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        raise Http404
    if experiment.lesson.teacher == request.user:
        student_list = {}
        return render(request, 'teacher/experiment_information.html',
                      {'student_list': student_list,
                       'experiment': experiment,
                       'experiment_id': experiment.id
                       })
    else:
        raise Http404


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def experiment_modify(request, experiment_id):
    try:
        experiment = Experiment.objects.get(
            id=experiment_id,
            lesson__teacher=request.user)
    except Experiment.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            experiment.name = form.cleaned_data['name']
            experiment.content = form.cleaned_data['content']
            experiment.deadline = form.cleaned_data['deadline']
            experiment.information = form.cleaned_data['information']
            experiment.save()
            return redirect('created_success')
        else:
            raise Http404
    else:
        return render(request,
                      'teacher/experiment_modify.html',
                      {'experiment': experiment})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def lesson_category_list(request):
    category_list = LessonCategory.objects.all()

    def _get_count(Category):
        count = Lesson.objects.filter(category=Category,
                                      teacher=request.user).count()
        setattr(Category, 'lesson_count', count)
        return count
    category_list = sorted(category_list, key=_get_count, reverse=True)
    return render(request, 'teacher/lesson_category_list.html',
                  {'category_list': category_list})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def lesson_information(request, lesson_id):
    teacher = request.user
    try:
        lesson = Lesson.objects.get(id=lesson_id, teacher=teacher)
    except Lesson.DoesNotExist:
        raise Http404
    experiment_list = Experiment.objects.filter(lesson=lesson)
    return render(request, 'teacher/lesson_information.html',
                  {'experiment_list': experiment_list,
                   'lesson': lesson,
                   'lesson_id': lesson_id
                   })


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def lesson_list(request, category_id):
    try:
        category = LessonCategory.objects.get(id=category_id)
    except LessonCategory.DoesNotExist:
        raise Http404
    lesson_list = Lesson.objects.filter(teacher=request.user,
                                        category=category)
    return render(request, 'teacher/lesson_list.html',
                  {'lesson_list': lesson_list,
                   'category': category})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def lesson_list_all(request):
    lesson_list = Lesson.objects.filter(teacher=request.user)
    return render(request, 'teacher/lesson_list.html',
                  {'lesson_list': lesson_list})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def update_lesson(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id,
                                    teacher=request.user)
    except Lesson.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        updated_form = LessonForm(data=request.POST)
        if updated_form.is_valid():
            lesson.name = updated_form.cleaned_data['name']
            lesson.category = updated_form.cleaned_data['category']
            lesson.info = updated_form.cleaned_data['info']
            lesson.save()
            return redirect('created_success')
    else:
        categories = LessonCategory.objects.all()
        return render(request, 'teacher/update_lesson.html',
                      {'categories': categories,
                       'lesson': lesson})
