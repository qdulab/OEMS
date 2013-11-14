# -*- coding: utf-8 -*-

from django import template

from experiment.models import ExperimentReport

register = template.Library()

@register.simple_tag(name="get_experiment_score_for_student")
def get_experiment_score_for_student(experiment, student):
    try:
        return ExperimentReport.objects.get(student=student,
                                            experiment=experiment).score
    except ExperimentReport.DoesNotExist:
        return u"<span class='red'>未得分</span>"


