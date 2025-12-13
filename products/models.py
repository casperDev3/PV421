from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Ідентифікатор продукту")
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
