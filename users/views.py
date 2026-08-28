from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


User = get_user_model()


# Список пользователей + создание
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Получение / обновление / удаление одного пользователя
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
