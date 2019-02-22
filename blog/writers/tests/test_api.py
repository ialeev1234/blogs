from copy import deepcopy

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from blog.writers.models import Writers


class WritersTests(APITestCase):

    def setUp(self):
        self.nick_data = {'name': 'Nick', 'age': 30, 'email': 'nick@nick.com', 'address': "Nick's Home"}
        self.helen_data = {'name': 'Helen', 'age': 27, 'email': 'helen@helen.com', 'address': "Helen's home"}

    def test_create_writer(self):
        """
        Ensure we can Create a new object.
        """
        url = reverse('writers-list')
        response = self.client.post(url, self.nick_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Writers.objects.count(), 1)
        self.assertEqual(Writers.objects.get().name, self.nick_data['name'])

    def test_get_writers(self):
        """
        Ensure we can Read created objects.
        """
        self.client.post('/writers/', self.nick_data, format='json')
        response = self.client.get('/writers/1/')
        new_nick = deepcopy(self.nick_data)
        new_nick.update({'id': 1})
        self.assertEqual(response.data, new_nick)
        response = self.client.get('/writers/')
        self.assertEqual(response.json()['results'], [new_nick])

    def test_put_writer(self):
        """
        Ensure we can Update created object using PUT.
        """
        self.client.post('/writers/', self.nick_data, format='json')
        response = self.client.get('/writers/1/')
        new_nick = deepcopy(self.nick_data)
        new_nick.update({'id': 1})
        self.assertEqual(response.data, new_nick)
        self.client.put('/writers/1/', self.helen_data, format='json')
        response = self.client.get('/writers/')
        new_helen = deepcopy(self.helen_data)
        new_helen.update({'id': 1})
        self.assertEqual(response.json()['results'], [new_helen])

    def test_delete_writer(self):
        """
        Ensure we can Delete created object.
        """
        self.client.post('/writers/', self.nick_data, format='json')
        response = self.client.get('/writers/1/')
        new_nick = deepcopy(self.nick_data)
        new_nick.update({'id': 1})
        self.assertEqual(response.data, new_nick)
        self.client.delete('/writers/1/')
        response = self.client.get('/writers/')
        self.assertEqual(response.json()['results'], [])

    def test_required_fields(self):
        """
        Ensure we can not create object without required fields.
        """
        url = reverse('writers-list')
        response = self.client.post(url, {}, format='json')
        error = {
            'name': [ErrorDetail(string='This field is required.', code='required')],
            'age': [ErrorDetail(string='This field is required.', code='required')],
            'email': [ErrorDetail(string='This field is required.', code='required')],
            'address': [ErrorDetail(string='This field is required.', code='required')]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error)
