from rest_framework.pagination import PageNumberPagination


class ContentPagination(PageNumberPagination):
    """Пагинатор для содержимого"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryPagination(PageNumberPagination):
    """Пагинатор для разделов"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50