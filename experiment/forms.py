from django import forms


class LessonCategoryForm(forms.Form):
    lesson_category = forms.CharField(max_length=60)


class ExperimentForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    content = forms.CharField(max_length=60)
    deadline = forms.DateTimeField()
    information = forms.CharField()
    weight = forms.IntegerField(required=True)
