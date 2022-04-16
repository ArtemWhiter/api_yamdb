from users.models import User
from reviews.models import Title, Comment, Review, Category, Genre
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from django.db.models import Avg


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'rating')

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if not rating:
            return 'Нет оценок'
        return round(rating, 2)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)
        model = Review
        
    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Можно оставлять не более одного отзыва'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    
    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
        model = Comment
