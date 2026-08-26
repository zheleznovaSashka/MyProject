from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Content
from .serializers import CategorySerializer, ContentSerializer, ContentCreateUpdateSerializer
from .permissions import IsAuthorOrAdmin
from .pagination import ContentPagination, CategoryPagination


# ---------- Категории ----------
class CategoryListCreateView(generics.ListCreateAPIView):
    """Список и создание категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали, обновление, удаление категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ---------- Содержимое ----------
class ContentListCreateView(generics.ListCreateAPIView):
    """Список и создание содержимого"""
    queryset = Content.objects.all()
    pagination_class = ContentPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'author']
    search_fields = ['title', 'body']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ContentCreateUpdateSerializer
        return ContentSerializer

    def perform_create(self, serializer):
        # Автоматически устанавливаем автора
        serializer.save(author=self.request.user)


class ContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали, обновление, удаление содержимого"""
    queryset = Content.objects.all()
    permission_classes = [IsAuthorOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ContentCreateUpdateSerializer
        return ContentSerializer


# ---------- Фильтр по автору (для просмотра своих записей) ----------
class MyContentListView(generics.ListAPIView):
    """Список содержимого текущего пользователя"""
    serializer_class = ContentSerializer
    pagination_class = ContentPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Content.objects.filter(author=self.request.user)
