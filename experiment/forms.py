from django import forms
from experiment.models import Lesson
from django.forms import widgets
from models import LessonCategory

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


class ExperimentForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    content = forms.CharField(max_length=60, required=False)
    deadline = forms.DateTimeField(required=False)
    information = forms.CharField(required=False)
    weight = forms.IntegerField(required=True)
