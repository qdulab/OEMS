from django import forms

from teacher.models import TeacherProfile


class TeacherForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=36)


class TeacherProfileForm(forms.ModelForm):

    class Meta:
        model = TeacherProfile
        fields = ('address', 'mobile', 'QQ', 'blog')
