from django import template

from experiment.models import Lesson

register = template.Library()

@register.filter(name='lesson_count')
def lesson_count(lesson_category):
    return Lesson.objects.filter(category=lesson_category).count()
