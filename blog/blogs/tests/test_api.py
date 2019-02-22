from copy import deepcopy

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from blog.blogs.models import Blogs


class BlogsTests(APITestCase):

    def setUp(self):
        self.writer1 = {
            'name': 'Nick',
            'age': 30,
            'email': 'nick@nick.com',
            'address': "Nick's home"
        }
        self.article1_data = {
            'title': 'Article1', 'excerpt': 'ABC', 'text': 'AABBCC',
            'date_created': '2019-02-23', 'date_updated': '2019-02-23', 'writer': self.writer1}
        self.article2_data = {
            'title': 'Article2', 'excerpt': 'ABC2', 'text': 'AABBCC2',
            'date_created': '2019-02-23', 'date_updated': '2019-02-23', 'writer': self.writer1}
        self.blog1_data = {'title': 'Blog1', 'articles': []}
        self.blog2_data = {'title': 'Blog2', 'articles': []}
        self.blog3_data = {'title': 'Blog3', 'articles': [self.article1_data, self.article2_data]}

    def test_create_blog(self):
        """
        Ensure we can Create a new object.
        """
        url = reverse('blogs-list')
        response = self.client.post(url, self.blog1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blogs.objects.count(), 1)
        self.assertEqual(Blogs.objects.get().title, self.blog1_data['title'])

    def test_get_blogs(self):
        """
        Ensure we can Read created objects.
        """
        self.client.post('/blogs/', self.blog1_data, format='json')
        response = self.client.get('/blogs/1/')
        new_blog1 = deepcopy(self.blog1_data)
        new_blog1.update({'id': 1})
        self.assertEqual(response.data, new_blog1)
        response = self.client.get('/blogs/')
        self.assertEqual(response.json()['results'], [new_blog1])

    def test_patch_blog(self):
        """
        Ensure we can Update created object using PATCH.
        """
        self.client.post('/blogs/', self.blog1_data, format='json')
        response = self.client.get('/blogs/1/')
        new_blog1 = deepcopy(self.blog1_data)
        new_blog1.update({'id': 1})
        self.assertEqual(response.data, new_blog1)
        self.client.patch('/blogs/1/', {'title': 'New title'}, format='json')
        response = self.client.get('/blogs/')
        new_blog1.update({'title': 'New title'})
        del response.data['results'].serializer
        self.assertEqual(response.data['results'], [new_blog1])

    def test_delete_blog(self):
        """
        Ensure we can Delete created object.
        """
        self.client.post('/blogs/', self.blog1_data, format='json')
        response = self.client.get('/blogs/1/')
        new_blog1 = deepcopy(self.blog1_data)
        new_blog1.update({'id': 1})
        self.assertEqual(response.data, new_blog1)
        self.client.delete('/blogs/1/')
        response = self.client.get('/blogs/')
        self.assertEqual(response.json()['results'], [])

    def test_required_fields(self):
        """
        Ensure we can not create object without required fields.
        """
        url = reverse('blogs-list')
        response = self.client.post(url, {}, format='json')
        error = {
            'title': [ErrorDetail(string='This field is required.', code='required')],
            'articles': [ErrorDetail(string='This field is required.', code='required')]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error)

    def test_articles_retrieving(self):
        """
        Ensure we can retrieve list of related objects
        """
        self.client.post('/blogs/', self.blog3_data, format='json')
        response = self.client.get('/blogs/1/')
        new_blog1 = deepcopy(self.blog3_data)
        del response.data['id']
        del response.data.serializer
        for i in response.data['articles']:
            del i['id']
            del i['writer']['id']
        self.assertEqual(response.data, new_blog1)
        response = self.client.get('/blogs/1/articles/')
        del response.data.serializer
        for i in response.data:
            del i['id']
            del i['writer']['id']
        self.assertEqual(response.data, new_blog1['articles'])
