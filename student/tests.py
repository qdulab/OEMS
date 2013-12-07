from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings


@override_settings(AUTHENTICATION_BACKENDS=
                   ('django.contrib.auth.backends.ModelBackend',))
class StudentLoginLogoutTest(TestCase):
    def setUp(self):
        self.student = User(username='test')
        self.student.set_password('test')
        self.student.save()
        self.client = Client()

    def test_login_with_correct_info(self):
        response = self.client.post(reverse('student_signin'),
                                    {'username': 'test', 'password': 'test'})
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_login_with_incorrect_info(self):
        response = self.client.post(reverse('student_signin'),
                                    {'username': 'wrong', 'password': '1'})
        self.assertRedirects(response, reverse('student_index'))

    def test_login_and_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('student_signout'))
        self.assertRedirects(response, reverse('student_index'))


@override_settings(AUTHENTICATION_BACKENDS=
                   ('django.contrib.auth.backends.ModelBackend',))
class StudentProfileTest(TestCase):
    def setUp(self):
        self.student = User(username='test')
        self.student.set_password('test')
        self.student.save()
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_profile_exist(self):
        self.assertTrue(self.student.profile)
        self.assertEqual(self.student.profile.school_id, '')
        self.assertEqual(self.student.profile.grade, '')
        self.assertEqual(self.student.profile.class_num, '')
        self.assertEqual(self.student.profile.phone_num, '')
        self.assertEqual(self.student.profile.major, '')

    def test_modified_profile(self):
        response = self.client.post(reverse('update_student_profile'),
                                    {'school_id': 'school_id',
                                     'grade': 'grade',
                                     'major': 'major',
                                     'class_num': 'class_num',
                                     'phone_num': ''})
        self.assertEqual(response.content, '{"status_phrase": "ok"}')
        self.assertEqual(self.student.profile.school_id, 'school_id')
        self.assertEqual(self.student.profile.grade, 'grade')
        self.assertEqual(self.student.profile.major, 'major')
        self.assertEqual(self.student.profile.class_num, 'class_num')
        self.assertEqual(self.student.profile.phone_num, '')


    def test_modified_profile_illegally(self):
        response = self.client.post(reverse('update_student_profile'),
                                    {'school_id': 'school_id',
                                     'grade': 'grade',
                                     'major': 'major',
                                     'class_num': '',
                                     'phone_num': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"status_phrase": "fail"}')
        self.assertEqual(self.student.profile.school_id, '')
        self.assertEqual(self.student.profile.grade, '')
        self.assertEqual(self.student.profile.major, '')
        self.assertEqual(self.student.profile.class_num, '')
        self.assertEqual(self.student.profile.phone_num, '')
