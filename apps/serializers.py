from rest_framework import serializers
from apps.models import Author, Book, Language, Genre
from collections import OrderedDict

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


class RelatedLanguageSerializer(serializers.Serializer):
    class Meta:
        model = Language
        fields = ['name', 'url']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    genre = RelatedGenreSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'summary', 'author', 'genre', 'language', 'isbn']

    def create(self, validated_data):
        #author_data = validated_data.pop('author')
        #author = Author.objects.get(first_name=author_data.get('first_name'),last_name=author_data.get('last_name'))
        genres_data = validated_data.pop('genre', None)
        book = Book.objects.create(**validated_data)
        for genre_data in genres_data:
            genre = Genre.objects.get_or_create(name=genre_data['name'])
            book.genre.add(genre[0])
            book.save()
        return book