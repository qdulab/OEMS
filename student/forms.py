from django import forms
from student.models import UserProfile

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('school_id', 'grade', 'major', 'class_num', 'phone_num')


