from rest_framework import serializers
from .models import Category, Content, Question


class CategorySerializer(serializers.ModelSerializer):
    contents_count = serializers.IntegerField(
        source='contents.count',
        read_only=True
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'contents_count']


class ContentSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Content
        fields = ['id', 'title', 'body', 'category', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)


# ⚠️ ВАЖНО: ЭТИ КЛАССЫ ДОЛЖНЫ БЫТЬ!
class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов"""
    content_title = serializers.CharField(source='content.title', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'content', 'content_title', 'text', 'answer',
            'created_by', 'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления вопросов"""

    class Meta:
        model = Question
        fields = ['id', 'content', 'text', 'answer']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)