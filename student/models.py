from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    school_id = models.CharField(max_length=20, null=False, blank=False)
    grade = models.CharField(max_length=10, null=False, blank=False)
    major = models.CharField(max_length=30, null=False, blank=False)
    class_num = models.CharField(max_length=10, null=False, blank=False)
    phone_num = models.CharField(max_length=12, null=False,
                                 blank=True)
    created_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name = _('UserProfile')
        verbose_name_plural = _('UserProfiles')

    def __unicode__(self):
        return u"School Id: %s Grade: %s Major: %s Class: %s" % (
                self.school_id, self.grade, self.major, self.class_num)

User.profile = property(
    lambda u:UserProfile.objects.get_or_create(user=u)[0])
