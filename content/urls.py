from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    ContentListCreateView, ContentDetailView,
    MyContentListView,
    QuestionListCreateView, QuestionDetailView, MyQuestionsListView
)

urlpatterns = [
    # Категории
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Содержимое
    path('contents/', ContentListCreateView.as_view(), name='content-list'),
    path('contents/<int:pk>/', ContentDetailView.as_view(), name='content-detail'),

    # Мои записи
    path('my-contents/', MyContentListView.as_view(), name='my-contents'),

    # Вопросы
    path('questions/', QuestionListCreateView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('my-questions/', MyQuestionsListView.as_view(), name='my-questions'),
]
