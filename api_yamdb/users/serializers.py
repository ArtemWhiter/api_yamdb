from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User