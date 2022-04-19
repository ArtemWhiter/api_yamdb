from django.shortcuts import render
from rest_framework import filters, viewsets, permissions, mixins
from rest_framework.pagination import LimitOffsetPagination
from api.serializers import TitleSerializer, CommentSerializer, ReviewSerializer, CategorySerializer, GenreSerializer, UserSerializer, TitlePostSerializer
from django.shortcuts import get_object_or_404
import django_filters
from django_filters.rest_framework import DjangoFilterBackend


from reviews.models import Title, Comment, Category, Genre
from users.models import User
from .permissions import IsAdminOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    genre = django_filters.CharFilter(field_name="genre__slug")
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name="year")

    class Meta:
        model = Title
        fields = ["category", "genre", "name", "year"]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitlePostSerializer


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


class CategoryViewSet(mixins.CreateModelMixin, 
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'    


class GenreViewSet(mixins.CreateModelMixin, 
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'
