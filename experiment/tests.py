from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

from experiment.models import LessonCategory, Lesson, Experiment
import json
from teacher.models import Teacher


@override_settings(AUTHENTICATION_BACKENDS=
                   ('teacher.backends.TeacherBackend', ))
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
        json_content = json.loads(response.content)
        self.assertEqual(json_content["status"], "OK")
        LessonCategory.objects.get(name="test")

    def test_create_existed_category(self):
        response = self.client.post(reverse('create_lesson_category'),
                                    {'name': "existed"})
        self.assertEqual(response.status_code, 200)
        json_content = json.loads(response.content)
        self.assertEqual(json_content["status"], "fail")
        self.assertEqual(json_content["content"], "existed")

    def test_create_not_valid_category(self):
        response = self.client.post(reverse('create_lesson_category'))
        self.assertEqual(response.status_code, 200)
        json_content = json.loads(response.content)
        self.assertEqual(json_content["status"], "fail")
        self.assertEqual(json_content["content"], "not valid")


@override_settings(AUTHENTICATION_BACKENDS=
                   ('teacher.backends.TeacherBackend', ))
class TeacherExperimentTest(TestCase):
    def setUp(self):
        self.teacher = Teacher(username='test')
        self.teacher.set_password('test')
        self.teacher.save()
        self.client = Client()
        self.client.login(username='test', password='test')
        self.category = LessonCategory.objects.create(name='category')
        self.lesson = Lesson.objects.create(name='lesson',
                                            category=self.category,
                                            teacher=self.teacher, status=True)

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
        json_response = json.loads(response.content)
        self.assertEqual(json_response["status_phrase"], "ok")
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
        category = LessonCategory.objects.create(name='jokerLC')
        lesson = Lesson.objects.create(
            name='jokerL', category=category, teacher=teacher)
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
        self.experiment = Experiment.objects.create(
            name='name', lesson=self.lesson, weight=1)
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
        self.experiment = Experiment.objects.create(
            name='name', lesson=self.lesson, weight=1)
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
        self.experiment = Experiment.objects.create(
            name='name', lesson=self.lesson, weight=1)
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
        category = LessonCategory.objects.create(name='jokerLC')
        lesson = Lesson.objects.create(
            name='jokerL', category=category, teacher=teacher)
        experiment = Experiment.objects.create(
            name='jokerE', lesson=lesson, weight=1)
        response = self.client.post(
            reverse('delete_experiment', args=(experiment.id, )))


class LessonTestForTeacher(TestCase):

    def setUp(self):
        self.teacher = Teacher(username="teacher")
        self.teacher.set_password("123")
        self.teacher.save()
        self.category = LessonCategory.objects.create(name="LessonCategory")
        self.lesson = Lesson.objects.create(
            name="lesson",
            category=self.category,
            teacher=self.teacher)
        self.client.login(username="teacher", password="123")

    def test_create_lesson(self):
        response = self.client.post(reverse('create_lesson'),
                                    {'name': "new_lesson",
                                     'category': self.category.id,
                                     'info': 123})
        self.assertEqual(response.status_code, 200)
        json_content = json.loads(response.content)
        self.assertEqual(json_content["status_phrase"], "ok")
        lesson = Lesson.objects.get(name="new_lesson")
        self.assertEqual(lesson.category, self.category)
        self.assertEqual(lesson.info, "123")

    def test_update_lesson(self):
        response = self.client.post(
            reverse('update_lesson', args=(self.lesson.id, )),
            {"name": "new_lesson",
             "category": self.category.id,
             "info": "123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
        lesson = Lesson.objects.get(name="new_lesson")
        self.assertEqual(lesson.category, self.category)
        self.assertEqual(lesson.info, "123")

    def test_update_other_teacher_lesson(self):
        teacher = Teacher(username="new_teacher")
        teacher.set_password("123")
        teacher.save()
        category = LessonCategory.objects.create(name="new_LessonCategory")
        lesson = Lesson.objects.create(
            name="new_lesson",
            category=category,
            teacher=teacher)
        response = self.client.post(
            reverse('update_lesson', args=(lesson.id, )),
            {"name": "new_lesson",
             "category": category.id,
             "info": "123"})
        self.assertEqual(response.status_code, 404)

    def test_delete_lesson(self):
        response = self.client.post(
            reverse('delete_lesson', args=(self.lesson.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
        lesson = Lesson.objects.filter(name="lesson")
        self.assertFalse(lesson)

    def test_delete_other_teacher_lesson(self):
        teacher = Teacher(username="new_teacher")
        teacher.set_password("123")
        teacher.save()
        category = LessonCategory.objects.create(name="new_LessonCategory")
        lesson = Lesson.objects.create(
            name="new_lesson",
            category=category,
            teacher=teacher)
        response = self.client.post(
            reverse('delete_lesson', args=(lesson.id, )))
        self.assertEqual(response.status_code, 404)


@override_settings(AUTHENTICATION_BACKENDS=
                   ('django.contrib.auth.backends.ModelBackend',))
class LessonTestForStudent(TestCase):

    def setUp(self):
        self.teacher = Teacher(username="teacher")
        self.teacher.set_password("123")
        self.teacher.save()
        self.category = LessonCategory.objects.create(name="LessonCategory")
        self.lesson = Lesson.objects.create(
            name="lesson",
            category=self.category,
            teacher=self.teacher)
        self.student = User(username="student")
        self.student.set_password("123")
        self.student.save()
        self.client.login(username="student", password="123")

    def test_subscribe_lesson(self):
        response = self.client.post(
            reverse('student_subscribe_handle', args=(self.lesson.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'success')
        Lesson.objects.get(id=self.lesson.id).students.get(id=self.student.id)

    def test_subscribe_lesson_does_not_exist(self):
        response = self.client.post(
            reverse('student_subscribe_handle', args=(1000,)))
        self.assertEqual(response.status_code, 404)

    def test_subscribe_lesson_already_closed(self):
        self.lesson.status = False
        self.lesson.save()
        response = self.client.post(
            reverse('student_subscribe_handle', args=(self.lesson.id,)))
        self.assertEqual(response.status_code, 404)
        lesson = Lesson.objects.get(id=self.lesson.id)
        student = lesson.students.filter(id=self.student.id)
        self.assertFalse(student)

    def test_unsubscribe_lesson(self):
        self.client.post(
            reverse('student_subscribe_handle', args=(self.lesson.id,)))
        response = self.client.post(
            reverse('student_unsubscribe_handle', args=(self.lesson.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")
        student = Lesson.objects.get(
            id=self.lesson.id).students.filter(
            id=self.student.id)
        self.assertFalse(student)

    def test_unsubscribe_lesson_does_not_subscribe(self):
        response = self.client.post(
            reverse('student_unsubscribe_handle', args=(self.lesson.id,)))
        self.assertEqual(response.status_code, 404)
