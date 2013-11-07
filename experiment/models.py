from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from teacher.models import Teacher

class LessonCategory(models.Model):
    """
    OMES LessonCategory have attributes name and created_at
    """
    name = models.CharField(max_length=60, null=False, blank=False,
                            unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Lesson Category')
        verbose_name_plural = _('Lesson Categories')

    def __unicode__(self):
        return u"Lesson Category: %s Created_at: %s" % (self.name,
                                                        self.created_at)
    @property
    def count(self):
        return 1



class Lesson(models.Model):
    """
    OMES Lesson, have attributes name, category, teacher,
    status, info, students, create_at
    """
    category = models.ForeignKey(LessonCategory)
    name = models.CharField(null=False, blank=False, max_length=64)
    teacher = models.ForeignKey(Teacher)
    status = models.BooleanField(blank=False)
    info = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User)

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    def __unicode__(self):
        return u"Lesson: %s" % self.name


class Experiment(models.Model):
    name = models.CharField(blank=False, max_length=128)
    create_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    lesson = models.ForeignKey(Lesson)
    deadline = models.DateTimeField(blank=True, null=True)
    remark = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _('Experiment')
        verbose_name_plural = _('Experiments')

    def __unicode__(self):
        return u"Experiment: %s" % self.name
	

class ExperimentReport(models.Model):
    title = models.CharField(max_length=60, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    experiment = models.ForeignKey(Experiment)
    content = models.TextField(blank=True)
    update_at = models.DateTimeField(auto_now=True)
    score = models.PositiveSmallIntegerField(null=True, blank=True)
    student = models.ForeignKey(User)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Experiment_report')
        verbose_name_plural = _('Experiment_reports')
    
    def __unicode__(self):
        return u"Experiment_report: %s" % self.title


