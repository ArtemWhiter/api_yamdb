from django.shortcuts import render
from rest_framework import filters, viewsets, permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from api.serializers import TitleSerializer, CommentSerializer, ReviewSerializer, CategorySerializer, GenreSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title, Comment, Review, Category, Genre
from users.models import User
from .permissions import IsAdminOrReadOnly

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)

    def perform_update(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user, text="123")


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'