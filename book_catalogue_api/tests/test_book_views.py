import datetime
import json

import requests
from rest_framework import status
from django.test import Client
from django.urls import reverse
from apps.models import Book, Genre, Language, Author
from apps.serializers import BookSerializer, RelatedGenreSerializer, RelatedLanguageSerializer, RelatedAuthorSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

factory = APIRequestFactory()

class TestBook(APITestCase):

    def setUp(self):
        author = Author.objects.create(first_name='Jane', last_name='Austen',
                                       date_of_birth=datetime.date(1775,1,16),
                                       date_of_death=datetime.date(1817,7,18))
        language = Language.objects.create(name='English')
        genre = Genre.objects.create(name='Romance')
        self.book1 = Book.objects.create(title='Pride and Prejudice', price=9, summary="Pride and Prejudice",
                                         author=author, language=language, isbn="9780141192345")
        self.book1.genre.add(genre)

        self.valid_payload = {
            "title": "Emma",
            "price": 9,
            "summary": "Emma",
            "author": "http://testserver/authors/20/",
            "genre": [
                {
                    "name": "Romance",
                    "url": "http://testserver/genres/1/"
                }
            ],
            "language": {
                "name": "English",
                "url": "http://testserver/languages/1/"
            },
            "isbn": "9780141192478",
            "published_date": "1811-12-23"
        }

        self.valid_payload_update = {
            "title": "Pride and Prejudice",
            "price": 10,
            "summary": "Pride and Prejudice",
            "author": "http://testserver/authors/20/",
            "genre": [
                {
                    "name": "Romance",
                    "url": "http://testserver/genres/1/"
                }
            ],
            "language": {
                "name": "English",
                "url": "http://testserver/languages/1/"
            },
            "isbn": "9780141192400",
            "published_date": "1810-08-04"
        }

        self.invalid_payload = {
            "price": 9,
            "summary": "Emma",
            "genre": [
                {
                    "name": "Romance",
                    "url": "http://testserver/genres/1/"
                }
            ],
            "language": {
            },
            "isbn": "aaa"
        }

    def test_get_all_books(self):
        response = self.client.get(reverse('books'))
        request = factory.post(reverse('books'), {})
        books = Book.objects.all()
        serializer = BookSerializer(books, context={'request': request}, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_a_book(self):
        response = self.client.get(reverse('books', kwargs={'pk': self.book1.pk}))
        request = factory.post(reverse('books', kwargs={'pk': self.book1.pk}))
        book = Book.objects.get(pk=self.book1.pk)
        serializer = BookSerializer(book, context={'request': request}, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_an_invalid_genre(self):
        response = self.client.get(reverse('books', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_book(self):
        response = self.client.post(reverse('books'), data=json.dumps(self.valid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_book(self):
        response = self.client.post(reverse('books'), data=json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_book(self):
        response = self.client.delete(reverse('books', kwargs={'pk': self.book1.pk }))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_book(self):
        response = self.client.delete(reverse('books', kwargs={'pk': 200 }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_book(self):
        response = self.client.put(reverse('books', kwargs={'pk': self.book1.pk}),
                              data=json.dumps(self.valid_payload_update), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    '''def test_invalid_update_genre(self):
        response = self.client.put(reverse('books', kwargs={'pk': self.book1.pk}),
                                   data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)'''


