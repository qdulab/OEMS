from django import forms

from experiment.models import ExperimentReport
from student.models import UserProfile

class ReportSubmitForm(forms.ModelForm):

    class Meta:
        model = ExperimentReport
        fields = ('title', 'content')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('school_id', 'grade', 'major', 'class_num', 'phone_num')
