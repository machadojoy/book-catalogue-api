from rest_framework import serializers
from apps.models import Author, Book, Language, Genre
from collections import OrderedDict
from rest_framework.validators import UniqueValidator

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class RelatedAuthorSerializer(serializers.Serializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'url']

class RelatedGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'url']
        extra_kwargs = {
            'name': {'validators': []},
        }


class RelatedLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name', 'url']
        extra_kwargs = {
            'name': {'validators': []},
        }

class BookSerializer(serializers.HyperlinkedModelSerializer):
    genre = RelatedGenreSerializer(many=True)
    language = RelatedLanguageSerializer(many=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'summary', 'author', 'genre', 'language', 'isbn']

    def create(self, validated_data):
        language_data = validated_data.pop('language')
        language_name = None
        for key, value in language_data.items():
            language_name = value

        language = Language.objects.get_or_create(name=language_name)
        genres_data = validated_data.pop('genre', None)
        book = Book.objects.create(language=language[0], **validated_data)
        for genre_data in genres_data:
            genre = Genre.objects.get_or_create(name=genre_data['name'])
            book.genre.add(genre[0])
            book.save()
        return book