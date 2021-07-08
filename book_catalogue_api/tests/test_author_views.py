import datetime
import json

import requests
from rest_framework import status
from django.test import Client
from django.urls import reverse
from apps.models import Author
from apps.serializers import AuthorSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

factory = APIRequestFactory()

class TestAuthor(APITestCase):

    def setUp(self):
        self.author1 = Author.objects.create(first_name='Jane', last_name='Austen',
                                             date_of_birth=datetime.date(1775,1,16),
                                             date_of_death=datetime.date(1817,7,18))
        self.author2 = Author.objects.create(first_name='Charlott', last_name='Bronte',
                                             date_of_birth=datetime.date(1816,4,20),
                                             date_of_death=datetime.date(1855,3,31))

        self.valid_payload = {
            'first_name': 'Sylvia',
            'last_name': 'Plath',
            'date_of_birth': '1932-10-27',
            'date_of_death': '1963-02-11'
        }

        self.valid_payload_update = {
            'first_name': 'Charlotte',
            'last_name': 'Bronte',
            'date_of_birth': '1816-04-20',
            'date_of_death': '1855-03-31'
        }

        self.invalid_payload = {
            'date_of_birth': None
        }

    def test_get_all_authors(self):
        response = self.client.get(reverse('author-list'))
        request = factory.post(reverse('author-list'), {})
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, context={'request': request}, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_an_author(self):
        response = self.client.get(reverse('author-detail', kwargs={'pk': self.author1.pk}))
        request = factory.post(reverse('author-detail', kwargs={'pk': self.author1.pk}))
        author = Author.objects.get(pk=self.author1.pk)
        serializer = AuthorSerializer(author, context={'request': request}, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_an_invalid_author(self):
        response = self.client.get(reverse('author-detail', kwargs={'pk': 100 }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_author(self):
        response = self.client.post(reverse('author-list'), data=json.dumps(self.valid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_author(self):
        response = self.client.post(reverse('author-list'), data=json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_author(self):
        response = self.client.put(reverse('author-detail', kwargs={'pk': self.author2.pk }),
                              data=json.dumps(self.valid_payload_update), content_type='application/json')
        self.assertEqual(response.data["first_name"], 'Charlotte')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_author(self):
        response = self.client.put(reverse('author-detail', kwargs={'pk': self.author2.pk}),
                              data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_valid_delete_author(self):
        response = self.client.delete(reverse('author-detail', kwargs={'pk': self.author2.pk }))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_author(self):
        response = self.client.delete(reverse('author-detail', kwargs={'pk': 200 }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

