from django.http import HttpResponse
from django.test import TestCase
from django.test.client import Client

from experiment.models import LessonCategory, Lesson
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
        response = self.client.post('/teacher/category/create/',
                                    {'name': "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "success")

    def test_create_existed_category(self):
        response = self.client.post('/teacher/category/create/',
                                    {'name': "existed"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         "Category has already existed")

