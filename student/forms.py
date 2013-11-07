#!/usr/bin/env python
# coding=utf-8
from django import forms

from experiment.models import ExperimentReport

class ReportSubmitForm(forms.ModelForm):

    class Meta:
        model = ExperimentReport
        fields = ('title', 'content')
