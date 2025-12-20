from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Ідентифікатор продукту")
    # add relation to User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    # product fields
    name = models.CharField(max_length=255, verbose_name="Назва продукту")
    description = models.TextField(verbose_name="Опис продукту")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна продукту")
    is_available = models.BooleanField(default=True, verbose_name="Доступність продукту")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"
