from django import forms
from experiment.models import Lesson
from django.forms import widgets
from models import LessonCategory

class LessonForm(forms.ModelForm):
    name = forms.CharField(label='lesson_name',
                           widget=forms.TextInput(
                               attrs={'class': "form-control",
                                      'name': "lesson_name",
                                      'placeholder':
                                      "please input the lesson name"}))
    info = forms.CharField(label='lesson_info',
                           widget=forms.Textarea(
                               attrs={'class': "form-control",
                                      'name': "lesson_info",
                                      'placeholder':
                                      "please input your infomation"}))
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
