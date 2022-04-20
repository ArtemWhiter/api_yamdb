from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken


from api.permissions import IsAdminOnly
from api.serializers import (AdminUserCreateSerializer, CategorieSerializer,
                             CommentSerializer, GenreSerializer,
                             PostSerializer, TitleSerializer,
                             TokenObtainSerializer, UserCreateSerializer)
from api_yamdb.settings import ADMIN_EMAIL
from reviews.models import Categorie, Comment, Genre, Post, Title
from users.models import User


class AdminUserCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserCreateSerializer
    permission_classes = (IsAdminOnly, )

    def post(self, request, *args, **kwargs):
        serializer = AdminUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = get_object_or_404(
                User,
                username=serializer.validated_data['username']
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Yamdb api pesonal code',
                f'Please, save your pesonal code: {confirmation_code}',
                ADMIN_EMAIL,
                [serializer.validated_data['email']],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif User.objects.filter(username=request.data.get('username'),
                                 email=request.data.get('email')).exists():

            user = get_object_or_404(
                User,
                username=request.data.get('username'),
                email=request.data.get('email'),
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'api token',
                f'Please, save your pesonal code: {confirmation_code}',
                ADMIN_EMAIL,
                [user.email],
                fail_silently=False,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CategorieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
