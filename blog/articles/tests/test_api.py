from copy import deepcopy

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from blog.articles.models import Articles


class ArticlesTests(APITestCase):

    def setUp(self):
        self.writer1 = {
            'name': 'Nick',
            'age': 30,
            'email': 'nick@nick.com',
            'address': "Nick's home"
        }
        self.writer2 = {
            'name': 'Helen',
            'age': 27,
            'email': 'helen@helen.com',
            'address': "Helen's home"
        }
        self.article1_data = {
            'title': 'Article1', 'excerpt': 'ABC', 'text': 'AABBCC',
            'date_created': '2019-02-23', 'date_updated': '2019-02-23', 'writer': self.writer1}

    def test_create_article(self):
        """
        Ensure we can Create a new object.
        """
        url = reverse('articles-list')
        response = self.client.post(url, self.article1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Articles.objects.count(), 1)
        self.assertEqual(Articles.objects.get().title, self.article1_data['title'])
        self.assertEqual(Articles.objects.get().writer.name, self.writer1['name'])

    def test_get_articles(self):
        """
        Ensure we can Read created objects.
        """
        self.client.post('/articles/', self.article1_data, format='json')
        response = self.client.get('/articles/1/')
        new_article1 = deepcopy(self.article1_data)
        new_article1.update({'id': 1})
        new_article1['writer'].update({'id': 1})
        del response.data.serializer
        self.assertEqual(response.data, new_article1)
        response = self.client.get('/articles/')
        self.assertEqual(response.json()['results'], [new_article1])

    def test_patch_article(self):
        """
        Ensure we can Update created object using PATCH.
        """
        self.client.post('/articles/', self.article1_data, format='json')
        response = self.client.get('/articles/1/')
        new_article1 = deepcopy(self.article1_data)
        new_article1.update({'id': 1})
        new_article1['writer'].update({'id': 1})
        del response.data.serializer
        self.assertEqual(response.data, new_article1)
        self.client.patch('/articles/1/', {'title': 'QQWWEE'}, format='json')
        response = self.client.get('/articles/')
        new_article1.update({'title': 'QQWWEE'})
        del response.data['results'].serializer
        self.assertEqual(response.data['results'], [new_article1])

    def test_delete_article(self):
        """
        Ensure we can Delete created object.
        """
        self.client.post('/articles/', self.article1_data, format='json')
        response = self.client.get('/articles/1/')
        new_article1 = deepcopy(self.article1_data)
        new_article1.update({'id': 1})
        new_article1['writer'].update({'id': 1})
        del response.data.serializer
        self.assertEqual(response.data, new_article1)
        self.client.delete('/articles/1/')
        response = self.client.get('/articles/')
        self.assertEqual(response.json()['results'], [])

    def test_required_fields(self):
        """
        Ensure we can not create object without required fields.
        """
        url = reverse('articles-list')
        response = self.client.post(url, {}, format='json')
        error = {
            'title': [ErrorDetail(string='This field is required.', code='required')],
            'excerpt': [ErrorDetail(string='This field is required.', code='required')],
            'text': [ErrorDetail(string='This field is required.', code='required')],
            'date_created': [ErrorDetail(string='This field is required.', code='required')],
            'date_updated': [ErrorDetail(string='This field is required.', code='required')],
            'writer': [ErrorDetail(string='This field is required.', code='required')]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error)
