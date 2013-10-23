from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from teacher.models import Teacher

class LessonCategory(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Lesson Category')
        verbose_name_plural = _('Lesson Categories')

    def __unicode__(self):
        return u"Lesson Category: %s Created_at: %s" % (self.name, self.created_at)


class Lesson(models.Model):
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
    name = models.CharField(null=False, blank=False, max_length=128)
    create_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False, blank=True)
    lesson = models.ForeignKey(Lesson)
    deadline = models.DateTimeField(blank=True, null=True)
    remark = models.TextField(null=False, blank=True)
    
    
    class Meta:
        verbose_name = _('Experiment')
        verbose_name_plural = _('Experiments')

    def __unicode__(self):
        return u"Experiment: " % self.name
	
