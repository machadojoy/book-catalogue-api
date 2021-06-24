from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from apps import views

router = DefaultRouter()
router.register(r'languages', views.LanguageViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'authors', views.AuthorViewSet)
#router.register(r'books', views.BookList.as_view())

urlpatterns = [
    path(r'books', views.BooksList.as_view(), name='books'),
    path(r'books/<int:pk>', views.BookDetail.as_view(), name='books'),
    path('', include(router.urls)),
]