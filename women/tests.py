from http import HTTPStatus
from django.test import TestCase
from django.urls import path, reverse
from women.models import Women


# Create your tests here.
class GetPagesTestCase(TestCase):

    def setUp(self):
        pass

    def test_main_page(self):
        main = reverse('home')
        response = self.client.get(main)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_add_redirect_page(self):
        p = reverse('add_page')
        redirect_url = reverse('users:login') + '?next=' + p
        response = self.client.get(p)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def tearDown(self):
        pass
