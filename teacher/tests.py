#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
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
        response = self.client.post(reverse('teacher_signin'),
                                    {'username': 'test', 'password': 'test'})
        self.assertRedirects(response, reverse('teacher_dashboard'))

    def test_login_with_incorrect_info(self):
        response = self.client.post(reverse('teacher_signin'),
                                    {'username': 'wrong', 'password': '1'})
        self.assertRedirects(response, reverse('teacher_index'))

    def test_login_and_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('teacher_signout'))
        self.assertRedirects(response, reverse('teacher_index'))


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
        response = self.client.post(reverse('teacher_profile'),
                                    {'address': 'address',
                                     'QQ': 'qq',
                                     'mobile': 'mobile',
                                     'blog': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"status": "ok"}')
        self.assertEqual(self.teacher.profile.address, 'address')
        self.assertEqual(self.teacher.profile.QQ, 'qq')
        self.assertEqual(self.teacher.profile.mobile, 'mobile')
        self.assertEqual(self.teacher.profile.blog, '')

    def test_modified_profile_illegally(self):
        response = self.client.post(reverse('teacher_profile'),
                                    {'address': 'address',
                                     'QQ': 'qq',
                                     'mobile': 'mobile',
                                     'blog': 'aaaa'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"status": "fail"}')
        self.assertEqual(self.teacher.profile.address, '')
        self.assertEqual(self.teacher.profile.QQ, '')
        self.assertEqual(self.teacher.profile.mobile, '')
        self.assertEqual(self.teacher.profile.blog, '')
