from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Content, Question

User = get_user_model()


class CategoryModelTest(TestCase):
    """Тесты для модели Category"""

    def setUp(self):
        self.category = Category.objects.create(
            name='Тестовая категория',
            description='Описание тестовой категории'
        )

    def test_create_category(self):
        """Тест создания категории"""
        self.assertEqual(self.category.name, 'Тестовая категория')
        self.assertEqual(self.category.description, 'Описание тестовой категории')

    def test_category_str(self):
        """Тест строкового представления категории"""
        self.assertEqual(str(self.category), 'Тестовая категория')


class ContentModelTest(TestCase):
    """Тесты для модели Content"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Test123!'
        )
        self.category = Category.objects.create(
            name='Тестовая категория'
        )
        self.content = Content.objects.create(
            title='Тестовый контент',
            body='Тестовое содержимое',
            category=self.category,
            author=self.user,
            status='published'
        )

    def test_create_content(self):
        """Тест создания контента"""
        self.assertEqual(self.content.title, 'Тестовый контент')
        self.assertEqual(self.content.status, 'published')

    def test_content_str(self):
        """Тест строкового представления контента"""
        self.assertEqual(str(self.content), 'Тестовый контент')


class QuestionModelTest(TestCase):
    """Тесты для модели Question"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Test123!'
        )
        self.category = Category.objects.create(
            name='Тестовая категория'
        )
        self.content = Content.objects.create(
            title='Тестовый контент',
            body='Тестовое содержимое',
            category=self.category,
            author=self.user,
            status='published'
        )
        self.question = Question.objects.create(
            content=self.content,
            text='Тестовый вопрос?',
            answer='Тестовый ответ',
            created_by=self.user
        )

    def test_create_question(self):
        """Тест создания вопроса"""
        self.assertEqual(self.question.text, 'Тестовый вопрос?')
        self.assertEqual(self.question.answer, 'Тестовый ответ')

    def test_question_str(self):
        """Тест строкового представления вопроса"""
        self.assertIn('Тестовый вопрос', str(self.question))


class ContentAPITest(TestCase):
    """Тесты для API контента"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='Test123!'
        )
        self.category = Category.objects.create(
            name='Тестовая категория'
        )
        self.content = Content.objects.create(
            title='Тестовый контент',
            body='Тестовое содержимое',
            category=self.category,
            author=self.user,
            status='published'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_contents_list(self):
        """Тест получения списка контента"""
        response = self.client.get('/api/contents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_content_api(self):
        """Тест создания контента через API"""
        data = {
            'title': 'Новый контент',
            'body': 'Новое содержимое',
            'category': self.category.id,
            'status': 'published'
        }
        response = self.client.post('/api/contents/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Новый контент')

    def test_get_content_detail(self):
        """Тест получения деталей контента"""
        response = self.client.get(f'/api/contents/{self.content.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовый контент')

    def test_update_content(self):
        """Тест обновления контента"""
        data = {
            'title': 'Обновленный контент',
            'body': 'Обновленное содержимое',
            'category': self.category.id,
            'status': 'published'
        }
        response = self.client.put(f'/api/contents/{self.content.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Обновленный контент')

    def test_delete_content(self):
        """Тест удаления контента"""
        response = self.client.delete(f'/api/contents/{self.content.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class QuestionAPITest(TestCase):
    """Тесты для API вопросов"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='Test123!'
        )
        self.category = Category.objects.create(
            name='Тестовая категория'
        )
        self.content = Content.objects.create(
            title='Тестовый контент',
            body='Тестовое содержимое',
            category=self.category,
            author=self.user,
            status='published'
        )
        self.question = Question.objects.create(
            content=self.content,
            text='Тестовый вопрос?',
            answer='Тестовый ответ',
            created_by=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_get_questions_list(self):
        """Тест получения списка вопросов"""
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_question_api(self):
        """Тест создания вопроса через API"""
        data = {
            'content': self.content.id,
            'text': 'Новый вопрос?',
            'answer': 'Новый ответ'
        }
        response = self.client.post('/api/questions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'Новый вопрос?')

    def test_get_question_detail(self):
        """Тест получения деталей вопроса"""
        response = self.client.get(f'/api/questions/{self.question.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Тестовый вопрос?')

    def test_update_question(self):
        """Тест обновления вопроса"""
        data = {
            'content': self.content.id,
            'text': 'Обновленный вопрос?',
            'answer': 'Обновленный ответ'
        }
        response = self.client.put(f'/api/questions/{self.question.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Обновленный вопрос?')

    def test_delete_question(self):
        """Тест удаления вопроса"""
        response = self.client.delete(f'/api/questions/{self.question.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_my_questions(self):
        """Тест получения своих вопросов"""
        response = self.client.get('/api/my-questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)