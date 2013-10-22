from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Teacher(AbstractUser):
    """ OEMS Teacher, has all djanog.contrib.auth.models.User
        attributes and methods
    """

    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

