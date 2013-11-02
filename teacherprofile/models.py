from django.db import models

from teacher.models import Teacher


class TeacherProfile(models.Model):
    """
    OEMS TeacherProfile, have address, mobile, QQ, blog
    """
    teacher = models.OneToOneField(Teacher)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    QQ = models.CharField(max_length=20)
    blog = models.URLField()

    class Meta:
        verbose_name = ('TeacherProfile')
        verbose_name_plural = ('TeacherProfiles')

    def __unicode__(self):
        return u"Teacher: %s" % self.teacher


Teacher.profile = property(lambda u:TeacherProfile.objects.get_or_create(teacher=u)[0])
