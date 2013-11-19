from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

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
        response = self.client.post(
            reverse('create_experiment', args=(self.lesson.id, )),
            {'name': 'name',
             'content': 'content',
             'lesson': self.lesson,
             'deadline': '',
             'remark': 'remark',
             'weight': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
        experiment = Experiment.objects.get(name='name')
        self.assertEqual(experiment.content, 'content')
        self.assertEqual(experiment.lesson, self.lesson)
        self.assertIsNone(experiment.deadline)
        self.assertEqual(experiment.remark, 'remark')
        self.assertEqual(experiment.weight, 1)

    def test_create_experiment_not_mine(self):
        teacher = Teacher(username='jokerT')
        teacher.set_password('jokerT')
        teacher.save()
        category = LessonCategory(name='jokerLC')
        category.save()
        lesson = Lesson(name='jokerL', category=category, teacher=teacher)
        lesson.save()
        response = self.client.post(
            reverse('create_experiment', args=(lesson.id, )),
            {'name': 'name',
             'content': 'content',
             'lesson': lesson,
             'deadline': '',
             'remark': 'remark',
             'weight': 1})
        self.assertEqual(response.status_code, 404)

    def test_modified_experiment(self):
        self.experiment = Experiment(name='name', lesson=self.lesson, weight=1)
        self.experiment.save()
        response = self.client.post(
            reverse('experiment_modify', args=(self.experiment.id, )),
            {'name': 'new_name',
             'content': 'new_content',
             'deadline': '',
             'remark': 'new_remark',
             'weight': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
        experiment = Experiment.objects.get(name='new_name')
        self.assertEqual(experiment.content, 'new_content')
        self.assertIsNone(experiment.deadline)
        self.assertEqual(experiment.remark, 'new_remark')
        self.assertEqual(experiment.weight, 2)

    def test_modified_profile_illegally(self):
        self.experiment = Experiment(name='name', lesson=self.lesson, weight=1)
        self.experiment.save()
        response = self.client.post(
            reverse('experiment_modify', args=(self.experiment.id, )),
            {'name': 'abcabcabcabcabcabcabcabcabcabcabc\
                     bcabcabcabcabcabcabcabcabcabcabcab\
                     cabcabcabcabcabcabcabcabcabcabcabc\
                     abcabcabcabcabcabcabcabcabcabcabca',
             'content': '',
             'deadline': '',
             'remark': 'new_remark',
             'weight': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "fail")

    def test_delete_experiment(self):
        self.experiment = Experiment(name='name', lesson=self.lesson, weight=1)
        self.experiment.save()
        response = self.client.post(
            reverse('delete_experiment', args=(self.experiment.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
        experiment = Experiment.objects.filter(id=self.experiment.id)
        self.assertFalse(experiment)

    def test_delete_experiment_not_mine(self):
        teacher = Teacher(username='jokerT')
        teacher.set_password('jokerT')
        teacher.save()
        category = LessonCategory(name='jokerLC')
        category.save()
        lesson = Lesson(name='jokerL', category=category, teacher=teacher)
        lesson.save()
        experiment = Experiment(name='jokerE', lesson=lesson, weight=1)
        experiment.save()
        response = self.client.post(
            reverse('delete_experiment', args=(experiment.id, )))
        self.assertEqual(response.status_code, 404)
