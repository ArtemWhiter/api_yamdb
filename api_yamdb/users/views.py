import imp
from django.shortcuts import render
from pyparsing import Literal
from rest_framework import filters, viewsets


from .serializers import UserSerializer, UserListSerializer
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.permissions import IsAdminOnly, IsUserOrAdminOnly


class UserListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = LimitOffsetPagination


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserOrAdminOnly]
    queryset = User.objects.all()
    
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username',)
    #ordering_fields = ('results')
