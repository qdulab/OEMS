from django import forms

class LessonCategoryForm(forms.Form):
    lesson_category = forms.CharField(max_length=60)