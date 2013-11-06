#!/usr/bin/env python
# coding=utf-8
from django import forms


class ReportSubmitForm(forms.Form):
    title = forms.CharField(max_length=60, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True) 
