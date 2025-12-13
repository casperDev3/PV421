from rest_framework import viewsets, filters
from .models import Product
from .serializers import ProductSerializer, ProductsSidebarSerializer
from rest_framework.pagination import PageNumberPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = []

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filtering
    search_fields = ['name', 'description']

    # sorting
    ordering_fields = ['price', 'created_at']
    ordering = ['created_at']

    # pagination
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2


class ProductsSidebarViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSidebarSerializer
    # permission_classes = []
