#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import time

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils import simplejson, timezone

from experiment.models import Experiment, ExperimentReport, LessonCategory, Lesson
from experiment.forms import ExperimentForm, LessonCategoryForm
from experiment.forms import LessonForm
from teacher.utils import is_teacher


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_lesson_category(request):
    if request.method == 'POST':
        form = LessonCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            try:
                category = LessonCategory.objects.create(name=name)
            except IntegrityError:
                response = {"status": "fail",
                            "content": "existed"}
                return HttpResponse(simplejson.dumps(response))
            category.created_at = timezone.make_naive(
                category.created_at,
                timezone.get_current_timezone())
            response = {"id": category.id,
                        "datetime":
                        time.mktime(category.created_at.timetuple()),
                        "status": "OK"}
            return HttpResponse(simplejson.dumps(response))
        else:
            response = {"status": "fail",
                        "content": "not valid"}

            return HttpResponse(simplejson.dumps(response))
    return render(request, 'teacher/create_lesson_category.html',)


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def create_lesson(request):
    if request.method == 'POST':
        form = LessonForm(data=request.POST)
        if form.is_valid():
            form.save(teacher=request.user)
            return HttpResponse("success")
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
            try:
                lesson = Lesson.objects.get(id=lesson_id, teacher=request.user)
            except Lesson.DoesNotExist:
                raise Http404
            form.save(lesson)
            return HttpResponse("success")
        else:
            return HttpResponse("fail")
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
        return HttpResponse("success")
    else:
        raise Http404


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def delete_lesson(request, lesson_id):
    try:
        Lesson.objects.get(id=lesson_id, teacher=request.user).delete()
    except Lesson.DoesNotExist:
        raise Http404
    return HttpResponse("success")


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def experiment_information(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        raise Http404
    if experiment.lesson.teacher == request.user:
        experiment_report_list = ExperimentReport.objects.filter(
            experiment=experiment)
        return render(request, 'teacher/experiment_information.html',
                      {'experiment_report_list': experiment_report_list,
                       'experiment': experiment,
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
            experiment.remark = form.cleaned_data['remark']
            experiment.weight = form.cleaned_data['weight']
            experiment.save()
            return HttpResponse("success")
        else:
            return HttpResponse("fail")
    else:
        return render(request,
                      'teacher/experiment_modify.html',
                      {'experiment': experiment})


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def lesson_category_list(request):
    category_list = LessonCategory.objects.all().order_by('-created_at')

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
                   'lesson': lesson})


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
def list_all_lesson(request):
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
            return HttpResponse("success")
    else:
        categories = LessonCategory.objects.all()
        return render(request, 'teacher/update_lesson.html',
                      {'categories': categories,
                       'lesson': lesson})
