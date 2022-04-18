from asyncio import mixins
from rest_framework import generics
from django.shortcuts import get_object_or_404, render
from rest_framework import filters, viewsets
from api.serializers import TitleSerializer, CommentSerializer, PostSerializer, CategorieSerializer, GenreSerializer
from api.permissions import NewUserOnly, IsAdminOnly
from api_yamdb.settings import ADMIN_EMAIL
from .serializers import UserCreateSerializer, AdminUserCreateSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Title, Comment, Post, Categorie, Genre
from users.models import User
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
import uuid
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        #user = serializer.save()
        serializer.save()
        username=serializer.data['username']
        email=serializer.data['email']
        confirmation_code=str(uuid.uuid4()),
        #confirmation_code=serializer.data['confirmation_code']
        #confirmation_code=serializer.data[uuid.uuid4()]
        send_mail(
            'API pesonal code',
            f'Hi, {username}! Please, save your pesonal code: {confirmation_code}',
            ADMIN_EMAIL,
            [email],
            fail_silently=False,
        )
        #send_confirmation_code(user)
        #serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AdminUserCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserCreateSerializer
    #permission_classes = (IsAdminOnly, )
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = AdminUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(APIView):
    queryset = User.objects.all()
    #serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        #user = get_object_or_404(User, username=username, email=email)
        if serializer.is_valid():
            #user = get_object_or_404(
                #User, 
                #username=self.kwargs.get('username'),
                #email=self.kwargs.get('email')
            #)
            #print(user)
            #username = serializer.data['username']
            #email = serializer.data['email']
            #user = get_object_or_404(User, username=username, email=email)
            #confirmation_code=str(uuid.uuid4()),
            #send_mail(
                #'api token',
                #f'Please, save your pesonal code: {confirmation_code}',
                #ADMIN_EMAIL,
                #[serializer.data['email']],    
                #fail_silently=False,
            #)
            serializer.save()
            #serializer.save(user=user, )
            return Response(serializer.data, status=status.HTTP_200_OK)
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
