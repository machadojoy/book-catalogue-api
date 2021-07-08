from django.test import TestCase
from apps.models import Language, Genre, Author, Book
import datetime

class LanguageTest(TestCase):

    def setUp(self):
        language = Language.objects.create(name='English')
        Language.objects.create(name='Dutch')

        genre = Genre.objects.create(name='Romance')
        Genre.objects.create(name='Thriller')

        author = Author.objects.create(first_name='Jane', last_name='Austen', date_of_birth=datetime.date(1775, 1, 16),
                              date_of_death=datetime.date(1817, 7, 18))

        book = Book.objects.create(title='Pride and Prejudice', summary="Some summary", author=author, language=language,
                            isbn='9780141192475', price=10, published_date=datetime.date(1812, 1, 16))

        book.genre.add(genre)
        book.save()

    def test_language_name(self):
        language_english = Language.objects.get(name='English')
        language_dutch = Language.objects.get(name='Dutch')

        self.assertEqual(language_english.name, "English")
        self.assertEqual(language_dutch.name, "Dutch")

    def test_genre_name(self):
        genre_romance = Genre.objects.get(name='Romance')
        genre_thriller = Genre.objects.get(name='Thriller')

        self.assertEqual(genre_romance.name, "Romance")
        self.assertEqual(genre_thriller.name, "Thriller")

    def test_author_dob(self):
        author = Author.objects.get(first_name='Jane', last_name='Austen')
        self.assertEqual(author.date_of_birth, datetime.date(1775, 1, 16))

    def test_book(self):
        book = Book.objects.get(title='Pride and Prejudice')
        self.assertEqual(book.price, 10)
        self.assertEqual(len(book.genre.all()), 1)
