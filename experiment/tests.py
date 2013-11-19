from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

from datetime import datetime
from experiment.models import LessonCategory, Lesson, Experiment
from teacher.models import Teacher


class LessonCategoryTest(TestCase):
    def setUp(self):
        self.teacher = Teacher(username='nihaoma')
        self.teacher.set_password('wangfushu')
        self.teacher.save()
        self.client = Client()
        self.client.login(username='nihaoma', password='wangfushu')
        self.category = LessonCategory(name='existed')
        self.category.save()

    def test_create_lesson_category(self):
        response = self.client.post(reverse('create_lesson_category'),
                                    {'name': "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")

    def test_create_existed_category(self):
        response = self.client.post(reverse('create_lesson_category'),
                                    {'name': "existed"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         "Category has already existed")

'''
@override_settings(AUTHENTICATION_BACKENDS=
                   ('django.contrib.auth.backends.ModelBackend',))
class StudentExperimentTest(TestCase):
    def setUp(self):
        self.student = User(username='test')
        self.student.set_password('test')
        self.student.save()
        self.client = Client()
        self.client.login(username='test', password='test')
    def test_show_experiment_information(self):
'''


@override_settings(AUTHENTICATION_BACKENDS=
                   ('teacher.backends.TeacherBackend', ))
class TeacherExperimentTest(TestCase):
    def setUp(self):
        self.teacher = Teacher(username='test')
        self.teacher.set_password('test')
        self.teacher.save()
        self.client = Client()
        self.client.login(username='test', password='test')
        self.category = LessonCategory(name='category')
        self.category.save()
        self.lesson = Lesson(name='lesson', category=self.category,
                             teacher=self.teacher, status=True)
        self.lesson.save()

    def test_create_experiment(self):
        response = self.client.post(reverse('create_experiment',
                                            args=(self.lesson.id,)),
                                    {'name': 'name',
                                     #'create_at': datetime(2013, 11, 19, 7, 53, 47, 540461),
                                     'content': 'content',
                                     'lesson': self.lesson,
                                     #'deadline': datetime(2013, 11, 19, 7, 53, 47, 540461),
                                     'remark': 'remark',
                                     'weight': 1,})
        #self.assertRedirects(response, reverse("success"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
        experiment = Experiment.objects.get(name='name')
        #self.assertEqual(experiment.create_at, datetime(2013, 11, 19, 7, 53, 47, 540461))
        self.assertEqual(experiment.content, 'content')
        self.assertEqual(experiment.lesson, self.lesson)
        #self.assertEqual(experiment.deadline, datetime(2013, 11, 19, 7, 53, 47, 540461))
        self.assertEqual(experiment.remark, 'remark')
        self.assertEqual(experiment.weight, 1)

'''
    def test_experiment_exist(self):
        self.assertTrue(self.student.profile)
        self.assertEqual(self.student.profile.school_id, '')
        self.assertEqual(self.student.profile.grade, '')
        self.assertEqual(self.student.profile.class_num, '')
        self.assertEqual(self.student.profile.phone_num, '')
        self.assertEqual(self.student.profile.major, '')

    def test_show_experiment_information(self):


    def test_delete_experiment(self):


    def test_modified_experiment(self):
     response = self.client.post(reverse('update_student_profile'),
                                    {'school_id': 'school_id',
                                     'grade': 'grade',
                                     'major': 'major',
                                     'class_num': 'class_num',
                                     'phone_num': ''})
        self.assertRedirects(response, reverse('student_profile'))
        self.assertEqual(self.student.profile.school_id, 'school_id')
        self.assertEqual(self.student.profile.grade, 'grade')
        self.assertEqual(self.student.profile.major, 'major')
        self.assertEqual(self.student.profile.class_num, 'class_num')
        self.assertEqual(self.student.profile.phone_num, '')


    def test_modified_experiment_illegally(self):
    response = self.client.post(reverse('update_student_profile'),
                                    {'school_id': 'school_id',
                                     'grade': 'grade',
                                     'major': 'major',
                                     'class_num': '',
                                     'phone_num': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'fail')
        self.assertEqual(self.student.profile.school_id, '')
        self.assertEqual(self.student.profile.grade, '')
        self.assertEqual(self.student.profile.major, '')
        self.assertEqual(self.student.profile.class_num, '')
        self.assertEqual(self.student.profile.phone_num, '')
'''
