from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from reviews.models import Categorie, Comment, Genre, Post, Title
from users.models import User


class AdminUserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Can't create user 'me'")
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Can't create user 'me'")
        return data

    class Meta:
        model = User
        fields = ('username', 'email',)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True,)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )
    #role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Can't rename user to 'me'")
        return data


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


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
