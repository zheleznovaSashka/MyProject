from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """Модель раздела (категории)"""
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Content(models.Model):
    """Модель содержимого"""
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'В архиве'),
    )

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержание")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name="Раздел"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name="Автор"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Содержимое"
        verbose_name_plural = "Содержимое"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ⚠️ ВАЖНО: Question должен быть ОТДЕЛЬНЫМ классом, НЕ вложенным!
class Question(models.Model):
    """Модель вопросов"""
    content = models.ForeignKey(
        Content,  # <--- теперь можно без кавычек, т.к. Content уже определён
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Содержимое"
    )
    text = models.TextField(verbose_name="Текст вопроса")
    answer = models.TextField(blank=True, null=True, verbose_name="Ответ")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Создатель"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Вопрос к {self.content.title}: {self.text[:50]}..."
