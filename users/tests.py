from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserModelTest(TestCase):
    """Тесты для модели User"""

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'Test123!'
        }

    def test_create_user(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('Test123!'))

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='Admin123!'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)


class UserAPITest(TestCase):
    """Тесты для API пользователей"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='Test123!'
        )

    def test_get_users_list(self):
        """Тест получения списка пользователей"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_api(self):
        """Тест создания пользователя через API"""
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'NewPass123!',
            'bio': 'Test bio'
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')