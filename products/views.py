from django.core.serializers import serialize
from rest_framework import viewsets, filters
from .models import Product
from .serializers import ProductSerializer, ProductsSidebarSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsManagerCanOnlyCreateOrEdit
from notifications.signals import notify_on_product_update


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # permissions for CRUD operations
    permission_classes = [IsManagerCanOnlyCreateOrEdit]

    # Встановлюємо користувача при створенні продукту
    # BEFORE CREATE / ON CREATE
    def perform_create(self, serializer):
        print("ЗАПИТ НА СТВОРЕННЯ ПРОДУКТУ:")
        serializer.save(user=self.request.user)

    # BEFORE UPDATE / ON UPDATE
    def perform_update(self, serializer):
        print("ЗАПИТ НА ОНОВЛЕННЯ ПРОДУКТУ:")
        notify_on_product_update(sender=Product, instance=serializer.instance)


    # BEFORE DELETE / ON DELETE
    def perform_destroy(self,  instance):
        print("ЗАПИТ НА ВИДАЛЕННЯ ПРОДУКТУ:")


    # Кастомний шлях: отримати дорогі продукти (ціна > 1000) через /api/products/expensive/
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def expensive(self, request):
        expensive_products = Product.objects.filter(price__gt=1000)  # приклад фільтрації дорогих продуктів
        serializer = self.get_serializer(expensive_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def toggle(self, request, pk=None):
        product = self.get_object()
        product.is_available = not product.is_available
        product.save()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filtering
    search_fields = ['name', 'description']

    # sorting
    ordering_fields = ['price', 'created_at']
    ordering = ['created_at']

    # pagination
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10


class ProductsSidebarViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSidebarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
