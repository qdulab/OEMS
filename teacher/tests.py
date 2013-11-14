from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

from teacher.models import Teacher

@override_settings(AUTHENTICATION_BACKENDS=
                   ('teacher.backends.TeacherBackend', ))
class TeacherLoginLogoutTest(TestCase):
    def setUp(self):
        self.teacher = Teacher(username='test')
        self.teacher.set_password('test')
        self.teacher.save()
        self.client = Client()

    def test_login_with_correct_info(self):
        response = self.client.post('/teacher/signin/',
                                    {'username': 'test', 'password': 'test'})
        self.assertRedirects(response, '/teacher/dashboard/')

    def test_login_with_incorrect_info(self):
        response = self.client.post('/teacher/signin/',
                                    {'username': 'wrong', 'password': '1'})
        self.assertRedirects(response, '/teacher/')

    def test_login_and_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/teacher/signout/')
        self.assertRedirects(response, '/teacher/')


@override_settings(AUTHENTICATION_BACKENDS=
                   ('teacher.backends.TeacherBackend', ))
class TeacherProfileTest(TestCase):
    def setUp(self):
        self.teacher = Teacher(username='test')
        self.teacher.set_password('test')
        self.teacher.save()
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_profile_exist(self):
        self.assertTrue(self.teacher.profile)
        self.assertEqual(self.teacher.profile.mobile, '')
        self.assertEqual(self.teacher.profile.address, '')
        self.assertEqual(self.teacher.profile.QQ, '')
        self.assertEqual(self.teacher.profile.blog, '')

    def test_modified_profile(self):
        response = self.client.post('/teacher/profile/',
                                    {'address': 'address',
                                     'QQ': 'qq',
                                     'mobile': 'mobile',
                                     'blog': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'success')
        self.assertEqual(self.teacher.profile.address, 'address')
        self.assertEqual(self.teacher.profile.QQ, 'qq')
        self.assertEqual(self.teacher.profile.mobile, 'mobile')
        self.assertEqual(self.teacher.profile.blog, '')

    def test_modified_profile_illegally(self):
        response = self.client.post('/teacher/profile/',
                                    {'address': 'address',
                                     'QQ': 'qq',
                                     'mobile': 'mobile',
                                     'blog': 'aaaa'})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, 'success')
        self.assertEqual(self.teacher.profile.address, '')
        self.assertEqual(self.teacher.profile.QQ, '')
        self.assertEqual(self.teacher.profile.mobile, '')
        self.assertEqual(self.teacher.profile.blog, '')
