from django import forms
from django.forms import widgets

from experiment.models import Experiment, Lesson

class LessonForm(forms.ModelForm):

    def save(self, teacher, **kwargs):
        form = super(LessonForm, self).save(commit=False, **kwargs)
        form.teacher = teacher
        form.status = True
        form.save()

    class Meta:
        model = Lesson
        fields = ('name', 'category', 'info')


class LessonCategoryForm(forms.Form):
    name = forms.CharField(max_length=60)


class ExperimentForm(forms.ModelForm):

    def save(self, lesson, **kwargs):
        form = super(ExperimentForm, self).save(commit=False, **kwargs)
        form.lesson = lesson
        form.save()

    class Meta:
        model = Experiment
        fields = ('name', 'content', 'deadline', 'remark', 'weight')
