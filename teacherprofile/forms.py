from django import forms

from models import TeacherProfile

class TeacherProfileForm(forms.ModelForm):

    class Meta:
        model = TeacherProfile
        fields = ('teacher', 'address', 'phone')
