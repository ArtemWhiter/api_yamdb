import imp

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from pyparsing import Literal
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.permissions import IsAdminOnly, IsUserOrAdminOnly

from .models import User
from .serializers import UserListSerializer, UserSerializer


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
