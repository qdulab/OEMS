from django import forms


class LessonCategoryForm(forms.Form):
    name = forms.CharField(max_length=60)


class ExperimentForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    content = forms.CharField(max_length=60, required=False)
    deadline = forms.DateTimeField(required=False)
    information = forms.CharField(required=False)
    weight = forms.IntegerField(required=True)
