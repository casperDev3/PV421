# news/models.py
from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст новини")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Посилання на зображення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новина"
        verbose_name_plural = "Новини"
        ordering = ['-created_at'] # Сортування: найновіші зверху