from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

#from api.permissions import IsAdmin
from api.serializers import (AdminUserCreateSerializer, 
                             CommentSerializer, GenreSerializer,
                             TitleSerializer,
                             TokenObtainSerializer, UserCreateSerializer,
                             UserSerializer)
from api_yamdb.settings import ADMIN_EMAIL
from reviews.models import Comment, Genre, Title, User

from django.shortcuts import render
from rest_framework import filters, viewsets
from api.serializers import (TitleSerializer, CommentSerializer,
                             ReviewSerializer, CategorySerializer,
                             GenreSerializer, TitlePostSerializer)
from django.shortcuts import get_object_or_404

from reviews.models import Title, Comment, Review, Category, Genre
from .permissions import IsOwnerOrReadOnly, IsAdmin, IsModerator, IsSuperUser, CreateIsAdmin, IsAdminOrReadOnly, IsAuthOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserCreateSerializer
    permission_classes = (CreateIsAdmin, )
    pagination_class = PageNumberPagination

    lookup_field = 'username'

    def post(self, request, *args, **kwargs):
        serializer = AdminUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuthenticated or IsAdmin, )
    )
    def about_me(self, request):
        serializer = UserSerializer()
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        if User.objects.filter(
                username=request.data.get('username'),
                email=request.data.get('email'),
                ).exists():
            send_personal_code(request)
            return Response(request.data, status=status.HTTP_200_OK)

        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_personal_code(request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_personal_code(request, *args, **kwargs):
    user = get_object_or_404(
                User,
                username=request.data.get('username'),
                email=request.data.get('email'),
            )
    confirmation_code = default_token_generator.make_token(user)
    return send_mail(
                    'Yamdb api pesonal code',
                    f'Please, save your pesonal code: {confirmation_code}',
                    ADMIN_EMAIL,
                    [user.email],
                    fail_silently=False,
                )


class TokenObtain(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data["username"]
        )

        if default_token_generator.check_token(
                        user,
                        serializer.validated_data["confirmation_code"]):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    genre = django_filters.CharFilter(field_name="genre__slug")
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name="year")

    class Meta:
        model = Title
        fields = ["category", "genre", "name", "year"]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)

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


 #   def perform_update(self, serializer):
 #       title_id = self.kwargs['title_id']
 #       title = get_object_or_404(Title, pk=title_id)
 #       serializer.save(title=title, author=self.request.user)


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

#    def perform_update(self, serializer):
#        review_id = self.kwargs['review_id']
#        review = get_object_or_404(Review, pk=review_id)
#        serializer.save(review=review, author=self.request.user)


class CategoryViewSet(mixins.CreateModelMixin, 
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination # LimitOffsetPagination
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
    pagination_class = PageNumberPagination # LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'
