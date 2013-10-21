from django.contrib.auth.models import check_password

from teachers.models import Teacher

class TeacherBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            teacher = Teacher.objects.get(username=username)
        except Teacher.DoesNotExcept:
            return None
        if check_password(password, teacher.password):
            return teacher
        return None

    def get_user(self, teacher_id=None):
        try:
            return Teacher.objects.get(pk=teacher_id)
        except Teacher.DoesNotExcept:
            return None
