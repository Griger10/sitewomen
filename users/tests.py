from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.data = data = {
            'username': 'user_1',
            'email': 'user1@sitewomen.ru',
            'first_name': 'Sergey',
            'last_name': 'Balakirev',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }

    def test_user_register(self):
        p = reverse('users:register')
        response = self.client.get(p)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_register_success(self):

        user_model = get_user_model()

        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())

    def test_user_registration_error(self):
        self.data['password2'] = '12345678A'
        user_model = get_user_model()

        path = reverse('users:register')
        response = self.client.post(path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_registration_exists_error(self):
        user_model = get_user_model()
        user_model.objects.create_user(username=self.data['username'])

        path = reverse('users:register')
        response = self.client.post(path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует')

    def tearDown(self):
        pass
