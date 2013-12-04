from django import template

from experiment.models import Lesson

register = template.Library()

@register.simple_tag
def lesson_count(lesson_category, teacher):
    return Lesson.objects.filter(category=lesson_category,
                                 teacher=teacher).count()
