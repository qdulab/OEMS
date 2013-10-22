from django.contrib.auth.models import check_password

from teacher.models import Teacher

class TeacherBackend(object):
    """ Teacher Model Auth Backend """

    def authenticate(self, username=None, password=None):
        """ Only when username exists in Teacher and the password is correct,
            return the teacher object
            else return None
        """
        try:
            teacher = Teacher.objects.get(username=username)
        except Teacher.DoesNotExcept:
            return None
        if check_password(password, teacher.password):
            return teacher
        return None

    def get_user(self, teacher_id=None):
        """ Get Teacher instance by pk, teacher_id is pk"""
        try:
            return Teacher.objects.get(pk=teacher_id)
        except Teacher.DoesNotExcept:
            return None
