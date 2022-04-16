from django.shortcuts import render
from rest_framework import filters, viewsets
from api.serializers import (TitleSerializer, CommentSerializer,
                             ReviewSerializer, CategorySerializer,
                             GenreSerializer)
from django.shortcuts import get_object_or_404

from reviews.models import Title, Comment, Review, Category, Genre
from users.models import User
from .permisions import IsOwnerOrReadOnly, IsAdmin, IsModerator, IsSuperUser

#class UserViewSet(viewsets.ReadOnlyModelViewSet):
    #queryset = User.objects.all()
    #serializer_class = UserSerializer

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsOwnerOrReadOnly | IsAdmin | IsModerator | IsSuperUser,
    )

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
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsOwnerOrReadOnly | IsAdmin | IsModerator | IsSuperUser,
    )

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)

    def perform_update(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
