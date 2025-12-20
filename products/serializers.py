from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Поля, які ми повертаємо через API
        fields = ['id', 'user', 'name', 'description', 'price', 'is_available', 'created_at']

class ProductsSidebarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Поля для відображення в сайдбарі
        fields = ['id', 'user', 'name', 'price', 'is_available']