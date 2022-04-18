import uuid

from django.shortcuts import get_object_or_404
from users.models import User
from reviews.models import Title, Comment, Post, Categorie, Genre
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from api_yamdb.settings import ADMIN_EMAIL
from django.core.mail import send_mail


class AdminUserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Can't create user 'me'")
        return data

    #def create(self, validated_data):
        #user = User(**validated_data)
        #user.save()
        #return user


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    #confirmation_code = serializers.CharField()

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Can't create user 'me'")
        return data
    
    #def create(self, validated_data):
        #user = User(**validated_data)
        #confirmation_code=str(uuid.uuid4()),
        #confirmation_code=validated_data[str(uuid.uuid4())]
        #confirmation_code.save()
        #User.objects.update_or_create(username=validated_data['username'], email=validated_data['email'], confirmation_code='confirmation_code')
        #user = User.objects.update_or_create(**validated_data)
        #print(get_object_or_404(User, usename=validated_data.get['username']))
        #user = get_object_or_404(User, username=validated_data['username'])
        #if get_object_or_404(User, usename=validated_data.pop['username']):
           # print('OK!')
            #user = User(**validated_data)
            #user.save()
        #user = User(**validated_data)
        
       # username=validated_data['username']
        #email=validated_data['email']
        #confirmation_code=str(uuid.uuid4()),
        #send_mail(
            #'API pesonal code',
            #f'Hi, {username}! Please, save your pesonal code: {confirmation_code}',
            #ADMIN_EMAIL,
            #[validated_data['email']],
            #fail_silently=False,
        ##)
        #user.save()
        #print(validated_data.get('username'))
        #return validated_data, confirmation_code
        #return user



    class Meta:
        model = User
        fields = ('username', 'email',)
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Post

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categorie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre