from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from apps.models import Language, Genre, Author, Book
from rest_framework import generics, viewsets, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, Http404
from apps.serializers import LanguageSerializer, GenreSerializer, AuthorSerializer, BookSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    #pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = PageNumberPagination


class BooksList(views.APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, context={'request': request},many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(views.APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
