from django import forms

class LessonCategoryForm(forms.Form):
    name = forms.CharField(max_length=60)