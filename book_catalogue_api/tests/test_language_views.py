import json

import requests
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from apps.models import Book, Language, Genre, Author
from apps.serializers import BookSerializer, GenreSerializer, LanguageSerializer, AuthorSerializer
from rest_framework.test import APIRequestFactory

client = Client()
factory = APIRequestFactory()

class TestLanguage(TestCase):

    def setUp(self):
        self.language1 = Language.objects.create(name='English')
        self.language2 = Language.objects.create(name='Dutch')

        self.valid_payload = {
            'name': 'German'
        }

        self.invalid_payload = {
            'name': ''
        }

        self.valid_payload_update = {
            'name': 'Nederlands'
        }

    def test_get_all_languages(self):
        response = client.get(reverse('language-list'))
        request = factory.post(reverse('language-list'), {})
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, context={'request': request } ,many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_valid_language(self):
        response = client.get(reverse('language-detail', kwargs={'pk': self.language1.pk }))
        request = factory.post(reverse('language-detail', args={'pk': self.language1.pk }))
        language = Language.objects.get(pk=self.language1.pk)
        serializer = LanguageSerializer(language, context={'request': request })
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_an_invalid_language(self):
        response = client.get(reverse('language-detail', kwargs={'pk': 100 }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_language(self):
        response = client.post(reverse('language-list'), data=json.dumps(self.valid_payload),
                                       content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_language(self):
        response = client.post(reverse('language-list'), data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_language(self):
        response = client.put(reverse('language-detail', kwargs={'pk': self.language2.pk }),
                              data=json.dumps(self.valid_payload_update), content_type='application/json')
        self.assertEqual(response.data["name"], 'Nederlands')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_language(self):
        response = client.put(reverse('language-detail', kwargs={'pk': self.language2.pk}),
                              data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_language(self):
        response = client.delete(reverse('language-detail', kwargs={'pk': self.language2.pk }))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_language(self):
        response = client.delete(reverse('language-detail', kwargs={'pk': 200 }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




