from django.db import models

from teacher.models import Teacher


class TeacherProfile(models.Model):
    """
    OEMS TeacherProfile, have address, mobile, QQ, blog
    """
    teacher = models.OneToOneField(Teacher)
    address = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    QQ = models.CharField(max_length=20, blank=True)
    blog = models.URLField(blank=True)

    class Meta:
        verbose_name = ('TeacherProfile')
        verbose_name_plural = ('TeacherProfiles')

    def __unicode__(self):
        return u"Teacher: %s" % self.teacher


Teacher.profile = property(lambda u:TeacherProfile.objects.get_or_create(teacher=u)[0])
