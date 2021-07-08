import json

import requests
from rest_framework import status
from django.test import Client
from django.urls import reverse
from apps.models import Genre
from apps.serializers import GenreSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

factory = APIRequestFactory()

class TestGenre(APITestCase):

    def setUp(self):
        self.genre1 = Genre.objects.create(name='Thriller')
        self.genre2 = Genre.objects.create(name='Mystery')

        self.valid_payload = {
            'name': 'Romance'
        }

        self.invalid_payload = {
            'name': ''
        }

        self.valid_payload_update = {
            'name': 'Mysteries'
        }

    def test_get_all_genres(self):
        response = self.client.get(reverse('genre-list'))
        request = factory.post(reverse('genre-list'), {})
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, context={'request': request}, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_a_genre(self):
        response = self.client.get(reverse('genre-detail', kwargs={'pk': self.genre1.pk }))
        request = factory.post(reverse('genre-detail', kwargs={'pk': self.genre1.pk }))
        genres = Genre.objects.get(pk=self.genre1.pk)
        serializer = GenreSerializer(genres, context={'request': request}, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_an_invalid_genre(self):
        response = self.client.get(reverse('genre-detail', kwargs={'pk': 100 }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_genre(self):
        response = self.client.post(reverse('genre-list'), data=json.dumps(self.valid_payload),
                                       content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_genre(self):
        response = self.client.post(reverse('genre-list'), data=json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_genre(self):
        response = self.client.put(reverse('genre-detail', kwargs={'pk': self.genre2.pk}),
                              data=json.dumps(self.valid_payload_update), content_type='application/json')
        self.assertEqual(response.data["name"], 'Mysteries')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_genre(self):
        response = self.client.put(reverse('genre-detail', kwargs={'pk': self.genre2.pk}),
                              data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_genre(self):
        response = self.client.delete(reverse('genre-detail', kwargs={'pk': self.genre2.pk }))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_genre(self):
        response = self.client.delete(reverse('genre-detail', kwargs={'pk': 200 }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)