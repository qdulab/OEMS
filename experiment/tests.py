from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

from experiment.models import LessonCategory, Lesson
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
        self.assertEqual(response.content, "success")

    def test_create_existed_category(self):
        response = self.client.post(reverse('create_lesson_category'),
                                    {'name': "existed"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         "Category has already existed")


@override_settings(AUTHENTICATION_BACKENDS=
                   ('teacher.backends.TeacherBackend', ))
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
        self.assertEqual(response.content, "success")
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
