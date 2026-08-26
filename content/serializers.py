from rest_framework import serializers
from .models import Category, Content


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для разделов"""
    contents_count = serializers.IntegerField(
        source='contents.count',
        read_only=True
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'contents_count']


class ContentSerializer(serializers.ModelSerializer):
    """Сериализатор для содержимого"""
    author_username = serializers.CharField(
        source='author.username',
        read_only=True
    )
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'body', 'category', 'category_name',
            'author', 'author_username', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']


class ContentCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления содержимого"""

    class Meta:
        model = Content
        fields = ['id', 'title', 'body', 'category', 'status']

    def create(self, validated_data):
        # Автоматически устанавливаем автора
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)